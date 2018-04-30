import sys

def getEvents():
    events = []
    for event in sys.stdin:
        events.append(event)
    return events

def parsePlots():
    plots = []
    currPlot = []
    events = getEvents()
    for event in events:
        if not event in ["EOS\tEOS\tEOS\tEOS\n", "SOS\tSOS\tSOS\tSOS\n"]:
            currPlot.append(event)
        if event == "EOS\tEOS\tEOS\tEOS\n":
            plots.append(currPlot)
            currPlot = []
    return plots

def subdividePlot(length, plot):
    return [plot[i * length:(i + 1) * length] for i in range((len(plot) + length - 1) // length )]

def cutPlots(length):
    plots = parsePlots()
    output = []
    for plot in plots:
        start = subdividePlot(length,plot)[0]
        start.append("EOS\tEOS\tEOS\tEOS\n")
        start.insert(0, "SOS\tSOS\tSOS\tSOS\n")
        output.append("".join(start))
    return "".join(output)

def partitionPlots():
    plots = parsePlots()
    output = []
    for plot in plots:
        morePlots = subdividePlot(length,plot)
        conctMorePlots = []
        for plot in morePlots:
            plot.append("EOS\tEOS\tEOS\tEOS\n")
            plot.insert(0, "SOS\tSOS\tSOS\tSOS\n")
            conctMorePlots.append("".join(plot))
        output.append("".join(conctMorePlots))
    return "".join(output)


if __name__ == "__main__":
    length = int(sys.argv[1])
    if sys.argv[2] == "cut":
        print(cutPlots(length))
    else:
        print(partitionPlots())
