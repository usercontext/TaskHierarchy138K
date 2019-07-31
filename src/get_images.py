import json
from lxml import html
import requests
import csv

def lts(lis):
    return ' '.join(lis)

with open('../category_article.json') as f:
    data_root = json.load(f)

img_file = open('images.csv', 'a')

def recurse(data):
    if data["children"]:
        for i in data["children"]:
            recurse(i)

    print(data["name"])
    images_list = []
    for kk in data["content"]:
        stripped = kk["url"]
        print('\t' + kk["name"])
        page = requests.get(stripped)
        tree = html.fromstring(page.content)

        images = tree.xpath('//li[contains(@class, "hasimage")]')
        for image in images:
            url = lts(image.xpath('.//img/@src'))
            title = lts(image.xpath('.//b[@class="whb"]/text()'))
            desc = lts(image.xpath('.//div[@class="step"]/text()')).strip()
            points = list(map(str.strip, image.xpath('.//li//text()[not(contains(., "WH."))]')))
            point_list = lts([item for item in points if item != ''])
            img_file.write('"' + url + '", "' + title + '", "' + desc  + '", "' + point_list  + '"\n')


recurse(data_root)