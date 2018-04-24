import sys
import nltk

def stat():
    lines = "" 
    for line in sys.stdin:
        lines = lines + line
    print("Sentences: " + str(lines.count(".")))
    print("Events ~= " + str(3 * lines.count(".")))
    print("Unique Words: " + str(len(set(lines.split(" ")))))

    tokens = nltk.word_tokenize(lines)
    tokens = set(tokens)
    tagged = nltk.pos_tag(tokens)
    pos = map(lambda x : x[1], tagged)
    pronouns = filter(lambda x : x == "NNP" or x == "NNPS", pos)
    print("Pronouns count: " + str(len(list(pronouns))))

if __name__ == '__main__':
    stat()
