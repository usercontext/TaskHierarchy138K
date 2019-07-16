import random
import pandas as pd
import sklearn
import matplotlib.pyplot as plt 
import numpy as np
import seaborn
import json
import pickle
from pandas.io.json import json_normalize
from nltk.corpus import stopwords
import re
import time
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.base import clone

with open("bow_data.json") as file:
    json_ext = json.load(file)

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

def get_child_bow(json_obj, path=[]):
    path.append(json_obj["name"])
    bow_collect = []
            
    for i in json_obj["children"]:
        bow_collect.extend(get_child_bow(i, path[:]))
        
    for j in json_obj["content"]:
        if "meta" in j:
            bow_collect.append(j["meta"]["bow"])
            
    return bow_collect
        

with open('../category_article.json', 'r') as f:
    json_new = json.load(f)


def attach_bow(json_bow_obj, json_obj, path=[]):
    path.append(json_obj["name"])
            
    for i,j in zip(json_bow_obj["children"], json_obj["children"]):
        attach_bow(i,j, path[:])
        
    json_obj["bow"] = get_child_bow(json_bow_obj)
    
attach_bow(json_ext, json_new)

total_bow = []
def get_parent_bow(json_obj, path=[]):
    path.append(json_obj["name"])
            
    for i in json_obj["children"]:
        get_parent_bow(i, path[:])
        
    for j in json_obj["content"]:
        if "meta" in j:
            total_bow.append(j["meta"]["bow"])
            
get_parent_bow(json_ext)
total_bow  = set(total_bow)
len(total_bow)

nb = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', SGDClassifier(loss='modified_huber', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
              ])

def nested_parser_clf(json_obj, path=[]):
    path.append(json_obj["name"])
    json_obj["clf"] = clone(nb)
    
    for j in json_obj["content"]:
        if "meta" in j:
            j["meta"]["bow"] = clean_text(j["meta"]["bow"])
            
    for i in json_obj["children"]:
        nested_parser_clf(i, path[:])
    

nested_parser_clf(json_new)

def nested_parser_new_clf_train(json_obj, path=[]):
    path.append(json_obj["name"])
    print(path, end="")
    bow_collect = []
    for i in json_obj["children"]:
        bow_collect.extend(i["bow"])
    
    bow_collect = set(bow_collect)
    for i in json_obj["children"]:
        print(i["name"])
        output = set(i["bow"])
        if len(json_obj["children"])>1:
            falseex = list(bow_collect-output)
        else:
            falseex = random.sample(list(total_bow - set(output)), (int(len(output) * 2)))
        print(len(falseex), len(output))
        dft = pd.DataFrame(list(output), columns=['bow'])
        dft["labels"] = ['True']*len(dft)
        dff = pd.DataFrame(falseex, columns=['bow'])
        dff["labels"] = ['False']*len(dff)
        dat = dft.append(dff, ignore_index=True)
        dat = dat.sample(frac=1).reset_index(drop=True)
        X = dat.bow
        y = dat.labels
        i["clf"].fit(X, y)
        nested_parser_new_clf_train(i, path[:])

nested_parser_new_clf_train(json_new)


fil = open('mulclass.pkl', 'wb')

def save_hier_model(json_obj, path=[]):
    path.append(json_obj["name"])
    print(path)
    pickle.dump(json_obj["clf"], fil)
            
    for i in json_obj["children"]:
        save_hier_model(i, path[:])
        
save_hier_model(json_new)
