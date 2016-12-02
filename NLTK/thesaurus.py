from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
def synset(word):
    return wn.synsets(word)

from nltk.corpus import wordnet
syns = wordnet.synsets('beautiful')
for s in syns:
    for l in s.lemmas():
        print str(l.name) + " " + str(l.count())
