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

    # find root
    for token in doc:
        if token.dep_ == "ROOT":
            root = token

    exploreBranch(root)
    
    """ for s in subj:
        if len(dobj) == 0:
            event = createEvent(s, mainVerb, "", "")
            allEvents.append(event)
        else:
            
            for o in dobj:
                event = createEvent(s, mainVerb, o, "")
                allEvents.append(event)
    
    return allEvents """

def exploreBranch(node):
    print(node.text)
    subj = []
    verb = node.text
    dobj = []
    misc = []
    
    for child in node.children:
        print(child.text)
        print(child.dep_)
        # find subject
        if child.dep_ == "nsubj":
            subj.append(child.text)

        # find objects (direct and objects of preposition)
        if child.dep_ == "dobj":
            dobj.append(child.text)
        if child.dep_ == "prep":
            print(child.children)
            for gchild in child.children:
                if gchild.dep_ == "pobj":
                    dobj.append(child.text)

        # find misc. (indirect objects)
        if child.dep_ == "dative":
            misc.append(child.text)

        # find other verbs
        if child.dep_ == "conj":
            exploreBranch(child)

    for sub in subj:
        for do in dobj:
            event = createEvent(sub, verb, dobj, "")

    return event

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
