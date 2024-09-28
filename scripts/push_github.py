from github import Github
from github import Auth
from github.GithubException import UnknownObjectException, GithubException
import json
import requests
import os

author_name = "Synchroneyes"
repository_name = "mineralcontest-static-backend"
auth = Auth.Token(os.environ['TOKEN_GITHUB'])
git = Github(auth=auth)
config_files = {}
config_maps = {}
repo = git.get_repo(f"{author_name}/{repository_name}")
zip_folder = "./zips/"
map_folder = "./maps/"
file_folder = "./files/"

def load_config():
    global config_files
    global config_maps
    with open("maps.json", encoding='utf-8') as f:
        config_maps = json.loads(f.read())

    with open("files.json", encoding='utf-8') as f:
        config_files = json.loads(f.read())

def check_release_exists(release_tag):
    """
    Check if a specific release exists in a GitHub repository.

    Parameters:
    release_tag (str): The tag of the release to check.
    current_md5 (str): MD5 signature of the current release.

    Returns:
    bool: True if the release exists, False otherwise.
    """
   
    try:
       
        # Try to fetch the release by its tag
        release = repo.get_release(release_tag)
 
        # If the release exists, return True
        return True
    except UnknownObjectException:
        # If the release doesn't exist, return False
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def should_create_release(release_tag, current_md5):
    try:
       
        # Try to fetch the release by its tag
        release = repo.get_release(release_tag)
        words = release.body.split(" ")

        # If the release exists, return True
        return not current_md5 in words
    except UnknownObjectException:
        # If the release doesn't exist, return False
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def delete_release(release_tag):
    try:
       
        # Try to fetch the release by its tag
        release = repo.get_release(release_tag)
        release.delete_release()
        # If the release exists, return True
        return True
    except UnknownObjectException:
        # If the release doesn't exist, return False
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def publish_map_release(item):
    release_message = item['map_description']
    release_message += "\n\n"
    release_message += f"Signature: {item['md5_signature']}"
    try:      
        # Create the release
        release = repo.create_git_release(
            tag=item['map_folder_name'],
            name=item['map_folder_name'],
            message=release_message,
        )

        # Upload the asset
        file = release.upload_asset(zip_folder + item['map_file_name'])
        thumbnail = release.upload_asset(map_folder + item['map_folder_name'] + "/thumbnail.png")


        
        print(f"Release {item['map_folder_name']} has been created successfully.")
        return True
    except GithubException as e:
        print(f"An error occurred: {e}")
        return False

def publish_plugin_release(file_type, version, item):
    release_message = f"Signature: {item['md5_signature']}"
    try:      

        release = repo.create_git_release(
            tag=f"{file_type}-{version}",
            name=f"{file_type}-{version}",
            message=release_message,
        )

        # Upload the asset
        file = release.upload_asset(f"{file_folder}{file_type}/{version}/{item['file_name']}")
        file = release.upload_asset(f"{file_folder}{file_type}/{version}/server_version")


        
        print(f"Release {item['file_name']} has been created successfully.")
        return True
    except GithubException as e:
        print(f"An error occurred: {e}")
        return False

load_config()
for maps in config_maps:
    map_exist = check_release_exists(maps["map_folder_name"])
    create_release = should_create_release(maps["map_folder_name"], maps["md5_signature"])

    if not map_exist:
        print(f"Creating {maps['map_folder_name']}")
        publish_map_release(maps)
        continue
    
    if map_exist and create_release:
        print(f"Updating {maps['map_folder_name']}")
        delete_release(maps["map_folder_name"])
        publish_map_release(maps)

for file_type in config_files:
    for version in config_files[file_type]:
        release_exist = check_release_exists(f"f{file_type}-{version}")
        create_release = should_create_release(f"{file_type}-{version}", config_files[file_type][version]["md5_signature"])

        if not release_exist and create_release:
            print(f"Creating {file_type}-{version}")
            publish_plugin_release(file_type, version, config_files[file_type][version])
            continue
        
        if release_exist and create_release:
            print(f"Updating {file_type}-{version}")
            delete_release(f"{file_type}-{version}")
            publish_plugin_release(file_type, version, config_files[file_type][version])