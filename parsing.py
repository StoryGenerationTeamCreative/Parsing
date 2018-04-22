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
        print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])

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
