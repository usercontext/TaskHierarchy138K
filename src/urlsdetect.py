import re

with open("sitemap.txt", "r") as fh:
    data = []
    raw_data = fh.readlines()
    for line in raw_data:
        if re.match(r'^http', line):
            data.append(line)

with open("result.txt", "w") as fh:
    for item in data:
        fh.write("%s" % item)