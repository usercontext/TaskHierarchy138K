# TaskHierarchy138K

Please check the website for more details: [https://usercontext.github.io/TaskHierarchy138K/](https://usercontext.github.io/TaskHierarchy138K/)

## Hierarchical classifier
The task hierarchy consists of binary classifiers at each node individually trained on the respective wikihow datapoints as positive examples and sibling wikihow datapoints as negative examples. The incoming query is passed through this hierarchy in a top-down manner where each of these binary classifiers act as a gating mechanism.

### Demonstration


<!-- Download the classifier pkl file and unzip it in the exp folder. Link: -->


#### Train
Go to exp folder
```
cd exp
```
Download the Bag of Words data attached to the task hierarchy: https://drive.google.com/file/d/1iae6Wqg4_YcTNMQJDgXCLoE7nAK7hHhm/view?usp=sharing and unzip.
```
python3 tasktrain.py
```

#### Test
In the same path, open python3 shell and follow the instructions:
```
$ cd exp
$ python3
>>> import json
>>> with open('../category_article.json', 'r') as f:
...   json_new = json.load(f)
>>> from tasktest import load_hier_model, greedytrickle, beamtrickle, clean_text
>>> load_hier_model(json_new)
>>> greedytrickle(json_new, clean_text("how to bake a strawberry cake"))
['Food and Entertaining', 'Recipes', 'Baking', 'Cakes', 'Fruit Cakes']
>>> beamtrickle(json_new, clean_text("how to bake a strawberry cake"))
[['Food and Entertaining', 0.58, 0.58, ['Recipes', 0.91, 0.53], ['Baking', 0.82, 0.44], ['Cakes', 1.0, 0.44]], 
['Food and Entertaining', 0.58, 0.58, ['Recipes', 0.91, 0.53], ['Baking', 0.82, 0.44], ['Scones', 0.19, 0.08]], 
['Food and Entertaining', 0.58, 0.58, ['Recipes', 0.91, 0.53], ['Fruits and Vegetables', 0.19, 0.1], ['Berries', 0.79, 0.08]], 
['Food and Entertaining', 0.58, 0.58, ['Recipes', 0.91, 0.53], ['Baking', 0.82, 0.44], ['Donuts and Doughnuts', 0.15, 0.07]], 
['Food and Entertaining', 0.58, 0.58, ['Recipes', 0.91, 0.53], ['Baking', 0.82, 0.44], ['Buns', 0.12, 0.05]]]
```