import random
import pandas as pd
import sklearn
import matplotlib.pyplot as plt 
import numpy as np
import seaborn
import json
from pandas.io.json import json_normalize
import pickle
from nltk.corpus import stopwords
import re

fil = open('mulclass.pkl', 'rb')

def load_hier_model(json_obj, path=[]):
    path.append(json_obj["name"])
    print(path)
    json_obj["clf"] = pickle.load(fil)
            
    for i in json_obj["children"]:
        load_hier_model(i, path[:])

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

def greedytrickle(json_obj, bow):
    scores = []
    path = []
    for i in json_obj["children"]:
        scores.append(i["clf"].predict_proba([bow]).tolist()[0][1])

    if scores:
        num = scores.index(max(scores))
        path.append(json_obj["children"][num]["name"])
    
        path += greedytrickle(json_obj["children"][num], bow)
    
    return path

def beamtrickle(json_obj, bow, beam_width=5, beam_length=4):
    s1 = []
    s2 = []
    for i in json_obj["children"]:
        proba = i["clf"].predict_proba([bow]).tolist()[0][1]
        s1.append(([i["name"], round(proba,2), round(proba,2)], proba, i))
    s1 = sorted(s1, key=lambda x: x[1], reverse=True)[:beam_width]
#     path.append([l[0] for l in s1])
    
    for _ in range(beam_length-1):
        for ii in s1:
            for kk in ii[2]["children"]:
                path = ii[0][:]
                proba = kk["clf"].predict_proba([bow]).tolist()[0][1]
                path.append([kk["name"], round(proba,2), round(proba  * ii[1], 2)])
                s2.append((path, proba  * ii[1], kk))
        
        s2 = sorted(s2, key=lambda x: x[1], reverse=True)[:beam_width]
        s1[:] = s2
        s2[:] = []
            
    return [l[0] for l in s1]