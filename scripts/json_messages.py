import os
import string
import json
import hashlib


def write_json_file(json_content, file_name):
  with open(f"{file_name}.json", "w", encoding='utf-8') as file:
    json.dump(json_content, file, ensure_ascii=False, indent=4)


messages_dir = "./messages"

messages = {}

for plugin_version in os.listdir(messages_dir):
    folder_path = os.path.join(messages_dir, plugin_version)
    messages[plugin_version] = []
    for _messages in os.listdir(folder_path):
        local_messages = []
        content = ""
        with open(os.path.join(folder_path, _messages), encoding='utf-8') as f:
            content = f.read()
        
        messages[plugin_version].append(content)



write_json_file(messages, "messages")
