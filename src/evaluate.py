import nltk

hypothesis = "baseball player is throwing ball in game"
reference = "Pitch a baseball"
reference = reference.split(" ")
hypothesis = hypothesis.split(" ")
BLEUscore = nltk.translate.bleu_score.sentence_bleu([reference], hypothesis, weights = [1])
print(BLEUscore)