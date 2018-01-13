import csv

# Gets stock symbols
def getStockSymbols():
    stksymbol = []
    with open('files/NASDAQ.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            stksymbol.append(row[0])
    return stksymbol

def getStockName():
    stkName = []
    with open('files/NASDAQ.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            stkName.append(row[1])
    return stkName

def getMax(numlist):
    return max(numlist)

def getMin(numlist):
    return min(numlist)

class Stock:
    def __init__(self, symbol, json_dict):
        self.symbol = symbol
        self.json_dict = json_dict

    # Returns float array
    def getOpen(self, symbol, json_dict):
        for key in json_dict:
            timeseries = key
        opened = []
        for key, val in json_dict[timeseries].items():
            opened.append(val['1. open'])
        return list(map(float, opened))

    def getClose(self, symbol, json_dict):
        for key in json_dict:
            timeseries = key
        closed = []
        for key, val in json_dict[timeseries].items():
            closed.append(val['4. close'])
        return list(map(float, closed))

    # Returns string array
    def getOpenDate(self, symbol, json_dict):
        for key in json_dict:
            timeseries = key
        date = []
        for key in json_dict[timeseries]:
            date.append(key)
        return date


