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


files_dir = "./files"
messages_dir = "./messages"
author_name = "Synchroneyes"
repository_name = "mineralcontest-static-backend"

files = {}

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




write_json_file(files, "files")
