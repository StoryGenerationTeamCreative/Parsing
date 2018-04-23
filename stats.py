import sys

def stat():
    lines = "" 
    for line in sys.stdin:
        lines = lines + line
    print("Sentences: " + str(lines.count(".")))
    print("Events ~= " + str(3 * lines.count(".")))
    lines = lines.split(" ")
    print("Words: " + str(len(set(lines))))
if __name__ == '__main__':
    stat()
