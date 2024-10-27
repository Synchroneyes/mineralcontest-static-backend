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
config_blog = {}

def load_config():
    """Charge les configurations du blog à partir des fichiers JSON."""
    global config_blog
    with open("blog.json", encoding='utf-8') as f:
        config_blog = json.load(f)

def check_release_exists(release_tag):
    """Vérifie si une release de blog existe dans le dépôt."""
    try:
        repo.get_release(release_tag)
        return True
    except UnknownObjectException:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def should_create_release(release_tag, current_md5):
    """Détermine si une nouvelle release de blog doit être créée."""
    try:
        release = repo.get_release(release_tag)
        return current_md5 not in release.body.split(" ")
    except UnknownObjectException:
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def delete_release(release_tag):
    """Supprime une release de blog existante."""
    try:
        release = repo.get_release(release_tag)
        release.delete_release()
        return True
    except UnknownObjectException:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def publish_blog_release(item):
    """Crée une nouvelle release pour un article de blog."""
    release_message = f"Signature: {item['md5_signature']}"
    try:      
        release = repo.create_git_release(
            tag=item['blog_title'],
            name=item['blog_title'],
            message=release_message,
        )

        # Télécharge les actifs de la release
        release.upload_asset(os.path.join(file_folder, item['file_name']))

        print(f"Release {item['blog_title']} has been created successfully.")
    except GithubException as e:
        print(f"An error occurred: {e}")

# Exécution principale pour publier les releases de blog
load_config()
for item in config_blog:
    release_exist = check_release_exists(item['blog_title'])
    create_release = should_create_release(item['blog_title'], item["md5_signature"])

    if not release_exist and create_release:
        print(f"Creating {item['blog_title']}")
        publish_blog_release(item)
    elif release_exist and create_release:
        print(f"Updating {item['blog_title']}")
        delete_release(item["blog_title"])
        publish_blog_release(item)
