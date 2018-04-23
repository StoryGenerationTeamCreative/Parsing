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

    events = exploreBranch(root)
    return events

def exploreBranch(node):
    print(node.text)
    subj = []
    verb = node.text
    dobj = []
    misc = []

    # general idea, find everything related to current verb and recurse on other verbs found
    for child in node.children:
        # very good for debugging
        print(child.text, child.dep_, child.head.text, child.head.pos_, [gchild for gchild in child.children])
        # find subject
        if child.dep_ == "nsubj":
            subj.append(child.text)

        # find objects (direct and objects of preposition)
        if child.dep_ == "dobj":
            dobj.append(child.text)
        if child.dep_ == "prep":
            for gchild in child.children:
                print(gchild.text)
                if gchild.dep_ == "pobj":
                    dobj.append(gchild.text)

        # find misc. (indirect objects)
        if child.dep_ == "dative":
            misc.append(child.text)

        # find other verbs
        if child.dep_ == "conj":
            exploreBranch(child)
    
    for sub in subj:
        # TODO: add check for no dobj (code written in parsing.py)
        for do in dobj:
            event = createEvent(sub, verb, do, "")
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
