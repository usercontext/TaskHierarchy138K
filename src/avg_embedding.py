import json
# import spacy
import numpy as np
# import spacy
# nlp = spacy.load('en_core_web_lg')

with open('personal_embed.json') as f:
    data = json.load(f)


def rec_embedding(data, store=np.zeros(300)):
    print(data["name"])
    # print(data["personal_embed"])
    locstore = np.zeros(300)
    if data["children"]:
        for i in data["children"]:
            locstore += rec_embedding(i, locstore)
        data["avg_embed"] = np.divide(locstore, len(data["children"])).tolist()
        return data["avg_embed"]
    else:
        return data["personal_embed"]


# def rectify_nan(data):
#     print(data["name"])

#     if "children" in data:
#         for i in data["children"]:
#             rectify_nan(i)

#     if np.isnan(data["personal_embed"]).all():
#         data["personal_embed"] = nlp(data["name"]).vector.tolist()

rec_embedding(data)

# rectify_nan(data)

with open('avg_embed.json', 'w') as f:
    import re
    output = json.dumps(data, indent=4)
    f.write(re.sub(r'(?<=\d),\s+', ', ', output))