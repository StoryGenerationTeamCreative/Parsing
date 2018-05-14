import sys
from nltk.corpus import wordnet as wn

def abstract(word):
    if word == "EMPTYPARAM" or word == "EOS" or word == "SOS" or word == "CHAR":
        return word
    else:
        depth = 20 
        chain = getHypernymChain(word,depth)
        if chain ==[]:
            return word
        else:
            return chain[min(len(chain), depth)-1]
        print(chain)

def getHypernymChain(word,depth):
    synset = wn.synsets(word)
    chain = []
    while(not synset == []):
        chain.append(synset[0].lemmas()[0].name())
        synset = synset[0].hypernyms()
    return chain


def printEvent(event):
    print(event[0] + "\t", end="")
    print(event[1] + "\t", end ="")
    print(event[2] + "\t", end = "")
    print(event[3] + "\n", end = "")

for event in sys.stdin:
    words = event.split("\t")
    words[-1] = words[-1].replace("\r","")
    words[-1] = words[-1].replace("\n","")
    printEvent([abstract(words[0]), words[1], abstract(words[2]), abstract(words[3])])
