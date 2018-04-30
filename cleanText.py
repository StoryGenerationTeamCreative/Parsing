import json
import sys
import string

dictionary = " qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.!?\'\""

def clean(string):
    string = string.encode('ascii', errors = 'ignore').decode()
    
    return string

def main():
    data = ""
    for line in sys.stdin:
        data = data + line
    data = clean(data)

    print(data)

main()
