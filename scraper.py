import wikipedia
import re
from textstat.textstat import textstat


MIN_LEN = 150

def scrape():
    pages = wikipedia.page("List_of_romance_films").links
    plots = map(tryGetPlot, pages)
    nonEmpty = filter(lambda plot : plot != None, plots)
    longEnough = filter(lambda plot : len(plot) >= MIN_LEN, nonEmpty)
    noNewLines = map(lambda plot : plot.replace("\n", " "), longEnough)
    noActors = map(lambda plot: re.sub(r" ?\([^)]+\)", "", plot), noNewLines)
    readable = filter(lambda plot: textstat.flesch_reading_ease(plot) > 70, noActors) 
    cleaned = readable 
    return cleaned

def tryGetPlot(page):
    try:
        return wikipedia.page(page).section("Plot")
    except wikipedia.exceptions.PageError:
        return None

if __name__ == '__main__':
    list(map(print, scrape()))
