import numpy as np
import nltk
import spacy
import sys
import time
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

nlp = spacy.load('en')

def createEvent(s, v, o, m):
    event = [""] * 4
    event[0] = s
    event[1] = v
    if (o == ""):
        event[2] = "EMPTYPARAM"
    else:
        event[2] = o
    if (m == ""):
        event[3] = "EMPTYPARAM"
    else:
        event[3] = m
    return event

def parseSentence(data):
    doc = nlp(data)
    properNouns = []

    # find root
    for token in doc:
        # print(token.text, token.dep_, token.head.text, token.head.pos_, token.pos_, [child for child in token.children])
        if token.dep_ == "ROOT":
            root = token
        elif token.pos_ == "PROPN":
            properNouns.append(token.lemma_)

    try:
        root
    except NameError:
        # not a complete sentence, ignore.
        # print("nameError")
        return [], ""
    
    subj = []
    dobj = []
    misc = []
    events = exploreBranch(subj, root, dobj, misc)
    
    return events, properNouns

def single(node):
    if node.pos_ == "PRON":
        return node.text
    # elif node.pos_ == "PROPN":
    #   return "CHAR1"
    else:
        return node.lemma_

def exploreBranch(subj, node, dobj, misc):
    verb = node.lemma_
    
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
            for gchild in child.children:
                if gchild.dep_ == "amod":
                    misc.append(single(gchild))
                elif gchild.dep_ == "conj":
                    subj.append(single(gchild))
        # find objects (direct and objects of preposition, predicate nominatives and adjectives)
        elif child.dep_ == "dobj" or child.dep_ == "acomp" or child.dep_ == "attr":
            dobj.append(single(child))
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    dobj.append(single(gchild))
                elif gchild.dep_ == "amod":
                    misc.append(single(gchild))
                elif gchild.dep_ == "prep":
                    for baby in gchild.children:
                        if baby.dep_ == "pobj":
                            misc.append(single(baby))
                            for fetus in baby.children:
                                if fetus.dep_ == "conj":
                                    misc.append(single(fetus))
        elif child.dep_ == "prep":
            for gchild in child.children:
                if gchild.dep_ == "pobj":
                    dobj.append(single(gchild))
                    for baby in gchild.children:
                        if baby.dep_ == "conj":
                            dobj.append(single(baby))
                        elif baby.dep_ == "amod":
                            misc.append(single(baby))
        # find indirect objects and adverbs
        elif child.dep_ == "dative":
            misc.append(single(child))
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    misc.append(single(gchild))
                elif gchild.dep_ == "amod":
                    misc.append(single(gchild))
        elif child.dep_ == "advmod":
            misc.append(single(child))
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    misc.append(single(gchild))

        # handle negations
        elif child.dep_ == "neg":
            misc.append(single(child))

        # find other verbs, either conjunct or subordinate
        elif child.dep_ == "conj" or child.dep_ == "advcl":
            subEvents = exploreBranch(subj, child, dobj, misc)
            for event in subEvents:
                allEvents.append(event)
                break
    
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

    count = 0
    if node.dep_ != "ROOT":
        count = 1
    
    for su in subj:
        for do in dobj:
            for mi in misc:
                allEvents.append(createEvent(su, verb, do, mi))
                if len(allEvents) >= 2:
                    return allEvents
    
    return allEvents

def getData():
    data = ""
    for line in sys.stdin:
        data = data + line
    return data

def main():
    plainText = getData()
    stories = plainText.splitlines()
    numStories = len(stories)
    # print(data)

    # start_time = time.time()
    
    numSentences = 0
    numEvents = 0
    properNouns = []
    for story in stories:
        print("SOS\tSOS\tSOS\tSOS")
        data = story.split(".")
        numSentences += len(data) - 1
        for sentence in data:
            events, proper = parseSentence(sentence)
            for noun in proper:
                properNouns.append(noun)
            for event in events:
                print("%s\t%s\t%s\t%s" % (event[0], event[1], event[2], event[3]))
                numEvents += 1
        print("EOS\tEOS\tEOS\tEOS")

    numNouns = len(properNouns)
    
    # print((time.time() - start_time))
    print("number of Stories: %d" % (numStories))
    print("number of Sentences: %d" % (numSentences))
    print("number of Events: %d, Per Story: %.3f, Per Sentence: %.3f" % (numEvents, numEvents / numStories, numEvents / numSentences))
    print("number of unique proper nouns: %d" % (numNouns))

main()
