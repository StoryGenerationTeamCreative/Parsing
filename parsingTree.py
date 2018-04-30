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
            subj.append(child.lemma_)
            for gchild in child.children:
                if gchild.dep_ == "amod":
                    misc.append(gchild.lemma_)
                elif gchild.dep_ == "conj":
                    subj.append(gchild.lemma_)
                elif gchild.dep_ == "relcl":
                    subEvents = exploreBranch(subj, gchild, dobj, misc)
                    for event in subEvents:
                        allEvents.append(event)
        # find objects (direct and objects of preposition, predicate nominatives and adjectives)
        elif child.dep_ == "dobj" or child.dep_ == "acomp" or child.dep_ == "attr":
            dobj.append(child.lemma_)
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    dobj.append(gchild.lemma_)
                elif gchild.dep_ == "amod":
                    misc.append(gchild.lemma_)
                elif gchild.dep_ == "prep":
                    for baby in gchild.children:
                        if baby.dep_ == "pobj":
                            misc.append(baby.lemma_)
                            for fetus in baby.children:
                                if fetus.dep_ == "conj":
                                    misc.append(fetus.lemma_)
                                elif fetus.dep_ == "relcl":
                                    relS = [fetus.head.lemma_]
                                    relD = []
                                    relM = []
                                    subEvents = exploreBranch(relS, fetus, relD, relM)
                                    for event in subEvents:
                                        allEvents.append(event)
                elif gchild.dep_ == "relcl":
                    relS = [gchild.head.lemma_]
                    relD = []
                    relM = []
                    subEvents = exploreBranch(relS, gchild, relD, relM)
                    for event in subEvents:
                        allEvents.append(event)
        elif child.dep_ == "prep":
            for gchild in child.children:
                if gchild.dep_ == "pobj":
                    dobj.append(gchild.lemma_)
                    for baby in gchild.children:
                        if baby.dep_ == "conj":
                            dobj.append(baby.lemma_)
                        elif baby.dep_ == "amod":
                            misc.append(baby.lemma_)
                        elif baby.dep_ == "relcl":
                            relS = [baby.head.lemma_]
                            relD = []
                            relM = []
                            subEvents = exploreBranch(relS, baby, relD, relM)
                            for event in subEvents:
                                allEvents.append(event)

        # find indirect objects and adverbs
        elif child.dep_ == "dative":
            misc.append(child.lemma_)
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    misc.append(gchild.lemma_)
                elif gchild.dep_ == "amod":
                    misc.append(gchild.lemma_)
                elif gchild.dep_ == "relcl":
                    relS = [gchild.head.lemma_]
                    relD = []
                    relM = []
                    subEvents = exploreBranch(relS, gchild, relD, relM)
                    for event in subEvents:
                        allEvents.append(event)
        elif child.dep_ == "advmod":
            misc.append(child.lemma_)
            for gchild in child.children:
                if gchild.dep_ == "conj":
                    misc.append(gchild.lemma_)

        # handle negations
        elif child.dep_ == "neg":
            misc.append(child.lemma_)

        # find other verbs, either conjunct or subordinate
        elif child.dep_ == "conj" or child.dep_ == "advcl":
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
    distinctNouns = len(set(properNouns))
    
    # print((time.time() - start_time))
    print("number of Stories: %d" % (numStories))
    print("number of Sentences: %d" % (numSentences))
    print("number of Events: %d, Per Story: %.3f, Per Sentence: %.3f" % (numEvents, numEvents / numStories, numEvents / numSentences))
    print("number of proper nouns: %d, unique: %d" % (numNouns, distinctNouns))

main()
