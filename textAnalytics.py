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
    for x in range(setSize):
        if x % 4 == 0:
            sub.append(data[x])
        elif x % 4 == 1:
            ver.append(data[x])
        elif x % 4 == 2:
            obj.append(data[x])
        else:
            mis.append(data[x])
    a = Counter(sub)
    b = Counter(ver)
    c = Counter(obj)
    d = Counter(mis)
    print("most common subjects")
    print(a.most_common(30))
    print("most common verbs")
    print(b.most_common(30))
    print("most common objects")
    print(c.most_common(30))
    print("most common modifiers")
    print(d.most_common(30))

main()
