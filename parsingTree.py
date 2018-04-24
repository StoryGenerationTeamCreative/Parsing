import numpy as np
import nltk
import spacy
import sys
from nltk.stem.porter import PorterStemmer

def createEvent(s, v, o, m):
    event = [""] * 4
    event[0] = s
    verb = stem(v)
    event[1] = verb
    event[2] = o
    event[3] = m
    return event

def parseSentence(data):
    nlp = spacy.load('en')
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
    print(node.text, node.dep_, node.head.text, node.head.pos_, [child for child in node.children])

    # general idea, find everything related to current verb and recurse on other verbs found
    for child in node.children:
        # another debugging statement
        print(child.text, child.dep_, child.head.text, child.head.pos_, [gchild for gchild in child.children])
        
        # find subject
        if child.dep_ == "nsubj":
            subj.append(child.text)
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    subj.append(gchild.text)

        # find objects (direct and objects of preposition)
        if child.dep_ == "dobj":
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

def stem(data_string):
    porter_stemmer = PorterStemmer()
    out_str = ""
    words = data_string.split()
    for word in words:
        out_str += porter_stemmer.stem(word) + " "
    return out_str

def getData():
    """data = ""
    for line in sys.stdin:
        data = data + line"""
    return "John and Lisa go to the store and the park. John runs quickly and steadily at the park. While John runs, Lisa buys groceries."

def main():
    # data = getData().splitlines()
    data = getData().split(".")
    print(data)
    
    allEvents = []
    for sentence in data:
        print(sentence)
        events = parseSentence(sentence)
        for event in events:
            allEvents.append(event)
    print(allEvents)

main()
