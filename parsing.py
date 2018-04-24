import numpy as np
import nltk
import spacy
from nltk.stem.porter import PorterStemmer
from nltk.parse.stanford import StanfordDependencyParser
import sys

def createEvent(s, v, o, m):
    event = [""] * 4
    event[0] = s
    verb = stem(v)
    event[1] = verb
    event[2] = o
    event[3] = m
    return event

def findTree(data):
    nlp = spacy.load('en')
    doc = nlp(data)

    allEvents = []
    
    subj = []
    mainVerb = ""
    dobj = []
    misc = []
    
    for token in doc:

        # find subjects of main verb
        if token.dep_ == "nsubj" and token.head.dep_ == "ROOT":
            subj.append(token.text)
            
            for child in token.children:
                if child.dep_ == "conj":
                    subj.append(child.text)
                    

        # find objects of main verb and/or objects of prepositions relating to main verb
        if token.dep_ == "dobj" and token.head.dep_ == "ROOT":
            dobj.append(token.text)
            for child in token.children:
                if child.dep_ == "conj":
                    dobj.append(child.text)
        elif token.dep_ == "pobj" and token.head.head.dep_ == "ROOT":
            dobj.append(token.text)
            for child in token.children:
                if child.dep_ == "conj":
                    dobj.append(child.text)

        # find miscellaneous, currently indirect objects
        """ elif token.dep_ == "dative" and token.head.dep_ == "ROOT":
            misc.append(token.text)
            for child in token.children:
                if child.dep_ == "conj":
                    misc.append(child.text) """
        
        
        # find main verbs            
        if token.dep_ == "ROOT":
            mainVerb = token.text
            for child in token.children:
                if child.dep_ == "conj":
                    subVerb = child.text
                    print(subVerb)
                    tempS = []
                    tempO = []
                    tempM = []
                    for baby in child.children:
                        if baby.dep_ == "nsubj":
                            tempS.append(baby.text)
                        if baby.dep_ == "dobj":
                            tempO.append(baby.text)
                    if len(tempS) == 0:
                        tempS = subj
                    if len(tempO) == 0:
                        tempO = dobj
                    if len(tempM) == 0:
                        tempM = misc
                    for su in tempS:
                        if len(tempO) == 0:
                            event = createEvent(su, subVerb, "", "")
                            allEvents.append(event)
                        else:
                            for ob in tempO:
                                event = createEvent(su, subVerb, ob, "")
                                allEvents.append(event)
    
    for s in subj:
        if len(dobj) == 0:
            event = createEvent(s, mainVerb, "", "")
            allEvents.append(event)
        else:
            
            for o in dobj:
                event = createEvent(s, mainVerb, o, "")
                allEvents.append(event)
    
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
    

def main():
    allEvents = []
    for sentence in sys.stdin:
        events = findTree(sentence)
        for event in events:
            allEvents.append(event)
    print(allEvents)

main()
