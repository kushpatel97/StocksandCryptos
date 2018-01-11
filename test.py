import requests, json
import csv
stkSymbol = []
stkName = []
with open('files/NASDAQ.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        stkSymbol.append(row[0])
        stkName.append(row[1])

print(stkSymbol)