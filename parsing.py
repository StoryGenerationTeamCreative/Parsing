import numpy as np
# import spacy
import nltk
import spacy
from nltk.stem.porter import PorterStemmer
from nltk.parse.stanford import StanfordDependencyParser

def createEvent(s, v, o):
    event = [""] * 4
    event[0] = s
    verb = stem(v)
    event[1] = verb
    event[2] = o
    return event

def findTree(data):
    nlp = spacy.load('en')
    doc = nlp(data)

    allEvents = []
    
    subj = []
    mainVerb = ""
    dobj = []
    
    for token in doc:
        # print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])
        if token.dep_ == "ROOT":
            mainVerb = token.text
            for child in token.children:
                if child.dep_ == "conj":
                    subVerb = child.text
                    tempS = []
                    tempO = []
                    for baby in child.children:
                        if baby.dep_ == "nsubj":
                            tempS.append(baby.text)
                        if baby.dep_ == "dobj":
                            tempO.append(baby.text)
                    if len(tempS) == 0:
                        tempS = subj
                    for su in tempS:
                        for ob in tempO:
                            allEvents.append(createEvent(su, subVerb, ob))
        
        if token.dep_ == "nsubj" and token.head.dep_ == "ROOT":
            subj.append(token.text)
            for child in token.children:
                if child.dep_ == "conj":
                    subj.append(child.text)
                    
        
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

    for s in subj:
        for o in dobj:
            event = createEvent(s, mainVerb, o)
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
    # data = getData().splitlines()
    data = ['John and Lisa go to the store and the park', 'John goes to the supermarket and runs in the park', 'Abby writes a lab and Chris reads it']
    #for x in range(len(data)):
    #    data[x] = stem(data[x])
    # results = np.array(map(getPOS, data))
    for sentence in data:
        print(sentence)
        events = findTree(sentence)
        print(events)

main()
