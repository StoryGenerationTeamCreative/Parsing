import wikipedia
import re
from textstat.textstat import textstat
import sys


def scrape():
    references = []
    for reference in sys.stdin:
        references.append(reference)
    pages = flatten(map(lambda x : wikipedia.page(x).links, references))
    plots = map(tryGetPlot, pages)
    nonEmpty = filter(lambda plot : plot != None, plots)
    longEnough = filter(lambda plot : len(plot) >= 300, nonEmpty)
    noNewLines = map(lambda plot : plot.replace("\n", " "), longEnough)
    noActors = map(lambda plot: re.sub(r" ?\([^)]+\)", "", plot), noNewLines)
    readable = filter(lambda plot: textstat.flesch_reading_ease(plot) > 70, noActors) 
    cleaned = readable 
    return cleaned

flatten = lambda l: [item for sublist in l for item in sublist]

def tryGetPlot(page):
    try:
        return wikipedia.page(page).section("Plot")
    except: 
        return None

if __name__ == '__main__':
    list(map(print, scrape()))
