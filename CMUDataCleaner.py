import sys

for plot in sys.stdin:
    if len(plot) > 200:
        print(plot.split("\t")[1], end = '')

