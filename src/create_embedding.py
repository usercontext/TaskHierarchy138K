import json
import spacy
import numpy as np
nlp = spacy.load('en_core_web_lg')

with open("../category_article.json") as f:
    data = json.load(f)

def rec_embedding(data):
    embedding = np.zeros(300)
    print(data["name"])
    for i in data["content"]:
        embedding += nlp(i["name"]).vector
    embedding = np.divide(embedding, len(data["content"]))

    data["personal_embed"] = embedding.tolist()

    for i in data["children"]:
        rec_embedding(i)

rec_embedding(data)

with open('personal_embed.json', 'w') as f:
    import re
    output = json.dumps(data, indent=4)
    f.write(re.sub(r'(?<=\d),\s+', ', ', output))
