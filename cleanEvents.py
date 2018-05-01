import sys

dictionary = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
dictionary = list(dictionary)

def main():
    for line in sys.stdin:
        words = line.split("\t")
        words[3] = words[3][:-1]
        outline = ""
        legal = True
        count = 0
        for word in words:
            if all(c in dictionary for c in word):
                if count == 3:
                    outline += word
                else:
                    outline += word + "\t"
                count += 1
            else:
                legal = False
                break
            if len(word) == 1 and word != "I":
                legal = False
                break
        if legal:
            print(outline)
main()
