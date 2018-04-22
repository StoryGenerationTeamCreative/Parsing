import numpy as np
# import spacy
import nltk
import spacy
from nltk.stem.porter import PorterStemmer
from nltk.parse.stanford import StanfordDependencyParser

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
        if token.dep_ == "ROOT":
            root = token
            mainVerb = token.text

    for child in root.children:
        print(child.text)
    
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
    # data = getData().splitlines()
    data = ['John and Lisa go to the store and the park', 'John gave Ella and me a present and made us dinner', 'Before she cooks, Sally shops']
    #for x in range(len(data)):
    #    data[x] = stem(data[x])
    # results = np.array(map(getPOS, data))
    allEvents = []
    for sentence in data:
        print(sentence)
        events = findTree(sentence)
        for event in events:
            allEvents.append(event)
    print(allEvents)

main()
