from github import Github, Auth
from github.GithubException import UnknownObjectException, GithubException
import json
import os

# Configuration du dépôt GitHub
author_name = "Synchroneyes"
repository_name = "mineralcontest-static-backend"
auth = Auth.Token(os.environ['TOKEN_GITHUB'])
git = Github(auth=auth)
repo = git.get_repo(f"{author_name}/{repository_name}")

# Dossier de travail
file_folder = "./files/"
config_files = {}

def load_config():
    """Charge les configurations des fichiers à partir des fichiers JSON."""
    global config_files
    with open("files.json", encoding='utf-8') as f:
        config_files = json.load(f)

def check_release_exists(release_tag):
    """Vérifie si une release de fichier existe dans le dépôt."""
    try:
        repo.get_release(release_tag)
        return True
    except UnknownObjectException:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def should_create_release(release_tag, current_md5):
    """Détermine si une nouvelle release de fichier doit être créée."""
    try:
        release = repo.get_release(release_tag)
        return current_md5 not in release.body.split(" ")
    except UnknownObjectException:
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def delete_release(release_tag):
    """Supprime une release de fichier existante."""
    try:
        release = repo.get_release(release_tag)
        release.delete_release()
        return True
    except UnknownObjectException:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def publish_plugin_release(file_type, version, item):
    """Crée une nouvelle release pour un fichier."""
    release_message = f"Signature: {item['md5_signature']}"
    try:      
        release = repo.create_git_release(
            tag=f"{file_type}-{version}",
            name=f"{file_type}-{version}",
            message=release_message,
        )

        # Télécharge les actifs de la release
        release.upload_asset(os.path.join(file_folder, file_type, version, item['file_name']))
        release.upload_asset(os.path.join(file_folder, file_type, version, "server_version"))

        print(f"Release {item['file_name']} has been created successfully.")
    except GithubException as e:
        print(f"An error occurred: {e}")

# Exécution principale pour publier les releases de fichiers
load_config()
for file_type in config_files:
    for version in config_files[file_type]:
        release_exist = check_release_exists(f"{file_type}-{version}")
        create_release = should_create_release(f"{file_type}-{version}", config_files[file_type][version]["md5_signature"])

        if not release_exist and create_release:
            print(f"Creating {file_type}-{version}")
            publish_plugin_release(file_type, version, config_files[file_type][version])
        elif release_exist and create_release:
            print(f"Updating {file_type}-{version}")
            delete_release(f"{file_type}-{version}")
            publish_plugin_release(file_type, version, config_files[file_type][version])
