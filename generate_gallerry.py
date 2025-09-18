import os
import yaml

BASE = "assets/drawings"

def prettify(name):
    return name.replace("_", " ").replace("-", " ").title()

gallery = {"albums": []}

for album in sorted(os.listdir(BASE)):
    album_path = os.path.join(BASE, album)
    if not os.path.isdir(album_path):
        continue
    subalbums = []
    for sub in sorted(os.listdir(album_path)):
        sub_path = os.path.join(album_path, sub)
        if not os.path.isdir(sub_path):
            continue
        images = []
        for file in sorted(os.listdir(sub_path)):
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                images.append({
                    "file": f"{album}/{sub}/{file}",
                    "title": prettify(os.path.splitext(file)[0])
                })
        subalbums.append({"name": prettify(sub), "images": images})
    gallery["albums"].append({"name": prettify(album), "subalbums": subalbums})

with open("_data/gallery.yml", "w") as f:
    yaml.dump(gallery, f, sort_keys=False)
