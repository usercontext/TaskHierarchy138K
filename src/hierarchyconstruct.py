import json
from urllib.parse import unquote

with open('cate.csv') as f:
    data = f.readlines()

def make_child(root, s):
    flag = False
    for ii in root["children"]:
        if ii["name"] == s:
            return ii
    root["children"].append({"name": s, "children": [], "content": []})
    for ii in root["children"]:
        if ii["name"] == s:
            return ii

def str_from_url(url):
    return unquote(" ".join(url[24:].split('-')))

root = {"name": "Root", "children": [], "content": []}
rootcopy = root
count = 0

for i in data:
    count+=1
    rootcopy = root
    cate_tree = i.split(', ')[1].replace('"', '').split(' > ')[2:-1]
    print(str_from_url(i.split(', ')[0]))
    for j in cate_tree:
        rootcopy = make_child(rootcopy, j)
    rootcopy["content"].append({
        "name": str_from_url(i.split(', ')[0]),
        "url": i.split(', ')[0]
    })
    if count%500 == 0:
        with open('cate_article.json', 'w') as outfile:
            json.dump(root, outfile, indent=4)