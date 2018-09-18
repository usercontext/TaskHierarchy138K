import json

with open('cate_article.json') as f:
    data_root = json.load(f)

global count
count = 0


def dict_depth(d, depth=0):
    if not isinstance(d, dict) or not d:
        return depth
    return max(dict_depth(v, depth + 1) for k, v in d.iteritems())


def recurse(data, depth=0):
    global count
    if data["children"]:
        for i in data["children"]:
            recurse(i)
    else:
        count
        count+=1


recurse(data_root)
print(count)