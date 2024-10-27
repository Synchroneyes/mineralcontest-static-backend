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
author_name = "Synchroneyes"
repository_name = "mineralcontest-static-backend"
domain_name = "api.mc.monvoisin-kevin.fr"

maps = []


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

write_json_file(maps, "maps")
