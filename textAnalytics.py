from collections import Counter
import sys
import numpy as np

def main():
    data = ""
    for line in sys.stdin:
        data = data + line
    data = data.split()
    setSize = np.shape(data)[0]
    sub = []
    ver = []
    obj = []
    mis = []
    subjectRepeats = 0
    verbRepeats = 0
    objectRepeats = 0
    modifierRepeats = 0
    for x in range(setSize):
        if x % 4 == 0:
            sub.append(data[x])
            if x > 3 and data[x] == data[x - 4]:
                subjectRepeats += 1
        elif x % 4 == 1:
            ver.append(data[x])
            if x > 3 and data[x] == data[x - 4]:
                verbRepeats += 1
        elif x % 4 == 2:
            obj.append(data[x])
            if x > 3 and data[x] == data[x - 4]:
                objectRepeats += 1
        else:
            mis.append(data[x])
            if x > 3 and data[x] == data[x - 4]:
                modifierRepeats += 1
    a = Counter(sub)
    uniqueS = len(set(sub))
    b = Counter(ver)
    uniqueV = len(set(ver))
    c = Counter(obj)
    uniqueO = len(set(obj))
    d = Counter(mis)
    uniqueM = len(set(mis))
    print("most common subjects")
    print(a.most_common(30))
    print("most common verbs")
    print(b.most_common(30))
    print("most common objects")
    print(c.most_common(30))
    print("most common modifiers")
    print(d.most_common(30))
    print("unique subjects : %d, verbs : %d, objects : %d, modifiers : %d" % (uniqueS, uniqueV, uniqueO, uniqueM))
    print("event to event repeats, subjects : %d, verbs : %d, objects : %d, modifiers : %d" % (subjectRepeats, verbRepeats, objectRepeats, modifierRepeats))

main()

# number of stories
# average number of events per story
# average number of events per sentence
# most common words
# words that repeat from event to event
# how many times subject and verb repeat
# how many proper nouns
