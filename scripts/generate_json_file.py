import os
import string
import json
import hashlib


def write_json_file(json_content, file_name):
  with open(f"{file_name}.json", "w", encoding='utf-8') as file:
    json.dump(json_content, file, ensure_ascii=False, indent=4)

def get_size(path):
        size = os.path.getsize(path)
        if size < 1024:
            return f"{size} bytes"
        elif size < pow(1024,2):
            return f"{round(size/1024, 2)} KB"
        elif size < pow(1024,3):
            return f"{round(size/(pow(1024,2)), 2)} MB"
        elif size < pow(1024,4):
            return f"{round(size/(pow(1024,3)), 2)} GB"


maps_dir = "./maps"
zip_dir = "./zips"
files_dir = "./files"
messages_dir = "./messages"
blog_dir = "./blog"
author_name = "Synchroneyes"
repository_name = "mineralcontest-static-backend"
domain_name = "api.mc.monvoisin-kevin.fr"

maps = []
files = {}
messages = {}
blog = []

for folder_name in os.listdir(maps_dir):
    folder_path = os.path.join(maps_dir, folder_name)
    zip_path = f"{os.path.join(zip_dir, folder_name)}.zip"
    if os.path.isdir(folder_path):
        map_size = os.stat(zip_path).st_size
        map_size_display = get_size(zip_path)
        map_name = string.capwords(("".join(folder_name.split("mc_")[1:])).replace("_", " "))
        with open(f"{folder_path}/description.txt", encoding='utf-8') as f: map_description = f.read().rstrip()
        map_folder_name = folder_name
        map_file_name = f"{folder_name}.zip"
        _map = {
          "map_url": f"https://github.com/{author_name}/{repository_name}/releases/download/{folder_name}/{folder_name}.zip",
          "map_thumbnail": f"https://github.com/{author_name}/{repository_name}/releases/download/{folder_name}/thumbnail.png",
          "map_name": map_name,
          "map_description": map_description,
          "map_size": str(map_size),
          "map_size_display": map_size_display,
          "map_file_name": map_file_name,
          "map_folder_name": map_folder_name,
          "md5_signature": hashlib.md5(open(f"{zip_dir}/{map_file_name}", "rb").read()).hexdigest()
        }
        maps.append(_map)


for folder_name in os.listdir(files_dir):
    file_type = os.path.join(files_dir, folder_name)
    files[folder_name] = {}
    for file_version in os.listdir(file_type):
        for file in os.listdir(os.path.join(file_type, file_version)):
            if(file.endswith(".jar")):
                file_size = os.stat(os.path.join(file_type, file_version, file)).st_size
                with open(f"{files_dir}/{folder_name}/{file_version}/server_version", encoding='utf-8') as f: server_version = f.read().rstrip()
                _file = {
                    "file_url": f"https://github.com/{author_name}/{repository_name}/releases/download/{folder_name}-{file_version}/{file}",
                    "file_name": f"{folder_name}-{file_version} {file.replace('.jar', '')}",
                    "file_size": str(file_size),
                    "file_size_display": get_size(os.path.join(file_type, file_version, file)),
                    "file_name": file,
                    "file_version": file_version,
                    "file_server_version": server_version,
                    "md5_signature": hashlib.md5(open(os.path.join(file_type, file_version, file), "rb").read()).hexdigest()
                }
                files[folder_name][file_version] = _file

for plugin_version in os.listdir(messages_dir):
    folder_path = os.path.join(messages_dir, plugin_version)
    messages[plugin_version] = []
    for _messages in os.listdir(folder_path):
        local_messages = []
        content = ""
        with open(os.path.join(folder_path, _messages), encoding='utf-8') as f:
            content = f.read()
        
        messages[plugin_version].append(content)

for article in os.listdir(blog_dir):
    print(article)
    _article = {
        "article_title": article.replace(".md", "").replace("_", " ").replace('-', ' ').capitalize(),
        "article_url": f"https://{domain_name}/blog/{article}",
    }
    blog.append(_article)


write_json_file(maps, "maps")
write_json_file(files, "files")
write_json_file(messages, "messages")
write_json_file(blog, "blog")