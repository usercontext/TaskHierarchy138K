from lxml import html
import requests

with open('result.txt') as f:
    data = f.readlines()

for i in data[51372:]:
    try:
        stripped = i.rstrip('\n')
        page = requests.get(stripped)
        tree = html.fromstring(page.content)
        cate = tree.xpath('//ul[@class="Breadcrumbs"]/li/a/text()')
        print(cate)
        with open('cate.csv','a') as rep:
            netstr = ""
            for item in cate:
                netstr += item + " > "
            rep.write(stripped + ', "' + netstr + '"\n')
    except Exception as e:
        with open("error.txt", "a") as k:
            k.write(str(e) + i)