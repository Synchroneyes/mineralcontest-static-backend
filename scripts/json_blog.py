import os
import string
import json
import hashlib


def write_json_file(json_content, file_name):
  with open(f"{file_name}.json", "w", encoding='utf-8') as file:
    json.dump(json_content, file, ensure_ascii=False, indent=4)

blog_dir = "./blog"
domain_name = "api.mc.monvoisin-kevin.fr"

blog = []

for article in os.listdir(blog_dir):
    article_path = os.path.join(blog_dir, article)
    
    article_title = ""
    article_description = ""
    article_author = ""

    with open(article_path, encoding='utf-8') as f:
        in_metadata = False
        for line in f:
            line = line.strip()
            if line == "---":
                in_metadata = not in_metadata
                if not in_metadata:
                    break  
                continue
            if in_metadata:
                if line.startswith("title:"):
                    article_title = line.replace("title:", "").strip()
                elif line.startswith("description:"):
                    article_description = line.replace("description:", "").strip()
                elif line.startswith("author:"):
                    article_author = line.replace("author:", "").strip()

    if not article_title:
        article_title = article.replace(".md", "").replace("_", " ").replace('-', ' ').capitalize()
    
    _article = {
        "article_title": article_title,
        "article_url": f"https://{domain_name}/blog/{article}",
        "article_description": article_description,
        "article_author": article_author
    }
    blog.append(_article)


write_json_file(blog, "blog")