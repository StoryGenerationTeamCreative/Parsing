import numpy as np
import json
import nltk
import spacy
import sys
import time
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

nlp = spacy.load('en')
lmtzr = WordNetLemmatizer()
stmmr = PorterStemmer()

# possible optimization: initialize stmmr and/or lmmtzr once in main and pass as argument?

def createEvent(s, v, o, m):
    event = [""] * 4
    event[0] = stem(s)
    event[1] = stem(v)
    event[2] = stem(o)
    event[3] = stem(m)
    return event

def parseSentence(data):
    doc = nlp(data)

    # find root
    for token in doc:
        if token.dep_ == "ROOT":
            root = token

    try:
        root
    except NameError:
        # not a complete sentence, ignore.
        return []
    
    subj = []
    dobj = []
    misc = []
    events = exploreBranch(subj, root, dobj, misc)
    
    return events

def exploreBranch(subj, node, dobj, misc):
    verb = node.text

    allEvents = []

    superS = subj
    superO = dobj
    superM = misc

    subj = []
    dobj = []
    misc = []

    # debugging statement
    # print(node.text, node.dep_, node.head.text, node.head.pos_, [child for child in node.children])

    # general idea, find everything related to current verb and recurse on other verbs found
    for child in node.children:
        # another debugging statement
        # print(child.text, child.dep_, child.head.text, child.head.pos_, [gchild for gchild in child.children])
        
        # find subject
        if child.dep_ == "nsubj":
            subj.append(child.text)
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    subj.append(gchild.text)

        # find objects (direct and objects of preposition, predicate nominatives and adjectives)
        if child.dep_ == "dobj" or child.dep_ == "acomp" or child.dep_ == "attr":
            dobj.append(child.text)
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    dobj.append(gchild.text)
        if child.dep_ == "prep":
            for gchild in child.children:
                if gchild.dep_ == "pobj":
                    dobj.append(gchild.text)
                    for baby in gchild.children:
                        if baby.dep_ == "conj":
                            dobj.append(baby.text)

        # find indirect objects and adverbs
        if child.dep_ == "dative":
            misc.append(child.text)
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    misc.append(gchild.text)
        if child.dep_ == "advmod":
            misc.append(child.text)
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    misc.append(gchild.text)

        # find other verbs, either conjunct or subordinate
        if child.dep_ == "conj" or child.dep_ == "advcl":
            subEvents = exploreBranch(subj, child, dobj, misc)
            for event in subEvents:
                allEvents.append(event)
        

    if len(subj) == 0:
        subj = superS
        
    if len(dobj) == 0 and len(superO) == 0:
        dobj = [""]
    elif len(dobj) == 0:
        dobj = superO
        
    if len(misc) == 0 and len(superM) == 0:
        misc = [""]
    elif len(misc) == 0:
        misc = superM
    
    for sub in subj:
        for do in dobj:
            for mi in misc:
                allEvents.append(createEvent(sub, verb, do, mi))
    
    return allEvents
    

def getPOS(data_string):
    tokens = nltk.word_tokenize(data_string)
    tags = nltk.pos_tag(tokens)
    return tags

lmtzr = WordNetLemmatizer()
def lemma(data_string):
    return lmtzr.lemmatize(data_string)

stmmr = PorterStemmer()
def stem(data_string):
    return stmmr.stem(data_string)

def getData():
    data = ""
    for line in sys.stdin:
        data = data + line
    return data

def main():
    # data = getData().splitlines()
    data = getData().split(".")
    nlp = spacy.load('en')
    # print(data)

    # start_time = time.time()
    
    allEvents = []
    for sentence in data:
        events = parseSentence(sentence)
        for event in events:
            allEvents.append(event)

    print(allEvents)
    # print((time.time() - start_time))
    # json.dump(allEvents, sys.stdout)

main()
