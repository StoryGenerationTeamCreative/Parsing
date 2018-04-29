import sys
import spacy
from spacy import displacy

def getData():
    plots = []
    for plot in sys.stdin:
        plots.append(plot)
    return plots

VERBS = ["VERB"]
NOUNS = ["NOUN", "PRON", "PROPN"]

def getVerbs(words):
    return [word for word in words if word.pos_ in VERBS] 

def getNouns(words):
    return [word for word in words if word.pos_ in NOUNS]

def getAncestors(word):
    return list(word.ancestors) 

def getChildren(word):
    return list(word.children)

def getChildNouns(word):
    return getNouns(getChildren(word))

#Equivalent to getting the nouns in the subj phrase if given a noun
def getChildNouns(word):
    rootNouns = getNouns(getChildren(word))
    subNouns = []
    for noun in rootNouns:
        subNouns = subNouns + (getChildNouns(noun))
    return rootNouns + subNouns


if __name__ == "__main__":
    nlp = spacy.load("en")
    text = nlp("John, Mary, and Billy, went to the park. Sam and Connor walked their dog")
    spacy.displacy.serve(text, style='dep')
    #print(getChildNouns(getVerbs(text)[1]))
