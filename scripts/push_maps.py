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
zip_folder = "./zips/"
map_folder = "./maps/"
config_maps = {}

def load_config():
    """Charge les configurations des cartes à partir des fichiers JSON."""
    global config_maps
    with open("maps.json", encoding='utf-8') as f:
        config_maps = json.load(f)

def check_release_exists(release_tag):
    """Vérifie si une release de carte existe dans le dépôt."""
    try:
        repo.get_release(release_tag)
        return True
    except UnknownObjectException:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def should_create_release(release_tag, current_md5):
    """Détermine si une nouvelle release de carte doit être créée."""
    try:
        release = repo.get_release(release_tag)
        return current_md5 not in release.body.split(" ")
    except UnknownObjectException:
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def delete_release(release_tag):
    """Supprime une release de carte existante."""
    try:
        release = repo.get_release(release_tag)
        release.delete_release()
        return True
    except UnknownObjectException:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def publish_map_release(item):
    """Crée une nouvelle release pour une carte."""
    release_message = f"{item['map_description']}\n\nSignature: {item['md5_signature']}"
    try:      
        release = repo.create_git_release(
            tag=item['map_folder_name'],
            name=item['map_folder_name'],
            message=release_message,
        )

        # Télécharge les actifs de la release
        release.upload_asset(os.path.join(zip_folder, item['map_file_name']))
        release.upload_asset(os.path.join(map_folder, item['map_folder_name'], "thumbnail.png"))

        print(f"Release {item['map_folder_name']} has been created successfully.")
    except GithubException as e:
        print(f"An error occurred: {e}")

# Exécution principale pour publier les releases de cartes
load_config()
for maps in config_maps:
    map_exist = check_release_exists(maps["map_folder_name"])
    create_release = should_create_release(maps["map_folder_name"], maps["md5_signature"])

    if not map_exist:
        print(f"Creating {maps['map_folder_name']}")
        publish_map_release(maps)
    elif map_exist and create_release:
        print(f"Updating {maps['map_folder_name']}")
        delete_release(maps["map_folder_name"])
        publish_map_release(maps)
