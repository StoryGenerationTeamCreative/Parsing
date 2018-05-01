import sys

dictionary = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvx"

def main():
    for line in sys.stdin:
        words = line.split("\t")
        outline = ""
        legal = True
        for word in words:
            if any(c in word for c in dictionary):
                outline += word + "\t"
            else:
                legal = False
                break
            if len(word) == 1 and word != "I":
                legal = False
                break
        if legal:
            print(outline,end="")
main()
