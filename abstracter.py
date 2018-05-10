import sys

lines = []
for event in sys.stdin:
    lines.append(map(abstract, event.split("\t")))

def abstract(word):
    if word == "EMPTYPARAM" or word == "EOS" or word = "SOS":
        return word
    else:
        return word
