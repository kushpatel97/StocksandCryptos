from flask import Flask, render_template, url_for, redirect, request
import json
import requests

app = Flask(__name__)

@app.route('/index',methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/check',methods = ['POST', 'GET'])
def check():
    if request.method == 'POST':
        stock = request.form['stock']
        return redirect(url_for('daily', symbol = stock))
    else:
        stock = request.args.get('stock')
        return redirect(url_for('daily', symbol = stock))

@app.route('/daily/<symbol>', methods = ['POST', 'GET'])
def daily(symbol):
    function = 'TIME_SERIES_DAILY'
    json_dict = getResponse(symbol, function)
    openData = getOpen(symbol,json_dict)
    closeData = getClose(symbol, json_dict)
    date = getOpenDate(symbol, json_dict)
    maxOpen = getMax(openData)
    minOpen = getMin(openData)
    maxClose = getMax(closeData)
    minClose = getMin(closeData)
    return render_template('daily.html', openData=openData, closeData=closeData, symbol=symbol, date=date, maxOpen=maxOpen, minOpen=minOpen, maxClose=maxClose, minClose=minClose)

@app.route('/intraday/<symbol>', methods = ['POST', 'GET'])
def intraday(symbol):
    function = 'TIME_SERIES_INTRADAY'
    json_dict = getResponse(symbol, function)

    openData = getOpen(symbol,json_dict)
    closeData = getClose(symbol, json_dict)
    date = getOpenDate(symbol, json_dict)
    maxOpen = getMax(openData)
    minOpen = getMin(openData)
    maxClose = getMax(closeData)
    minClose = getMin(closeData)
    return render_template('intraday.html', openData=openData, closeData=closeData, symbol=symbol, date=date, maxOpen=maxOpen, minOpen=minOpen, maxClose=maxClose, minClose=minClose)

def getResponse(symbol, function):
    API_KEY = 'O2877FVGMXZ33X94'
    API_URL = 'https://www.alphavantage.co/query'
    if function == 'TIME_SERIES_INTRADAY':
        parameters = {
            'function': function,
            'symbol': symbol,
            'interval': '5min',
            'outputsize': 'compact',
            'apikey': API_KEY
        }
    else:
        parameters = {
            'function': function,
            'symbol': symbol,
            'apikey': API_KEY
        }
    json_data = requests.get(API_URL, params=parameters)
    json_dict = json.loads(json_data.content)
    return json_dict

# Returns float array
def getOpen(symbol,json_dict):
    for key in json_dict:
        timeseries = key
    opened = []
    for key, val in json_dict[timeseries].items():
        opened.append(val['1. open'])
    return list(map(float,opened))

def getClose(symbol, json_dict):
    for key in json_dict:
        timeseries = key
    closed = []
    for key, val in json_dict[timeseries].items():
        closed.append(val['4. close'])
    return list(map(float,closed))
# Returns string array
def getOpenDate(symbol,json_dict):
    for key in json_dict:
        timeseries = key
    date = []
    for key in json_dict[timeseries]:
        date.append(key)
    return date

def getMax(numlist):
    return max(numlist)

def getMin(numlist):
    return min(numlist)

if __name__ == '__main__':
    app.run(debug=True)