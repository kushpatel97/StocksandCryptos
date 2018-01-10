from flask import Flask, render_template, url_for, redirect, request
import json
import requests
import stock

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
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

@app.route('/stocks', methods = ['POST', 'GET'])
def stocks():
    return render_template('stocks.html')

@app.route('/cryptos', methods = ['POST', 'GET'])
def cryptos():
    return render_template('cryptos.html')

@app.route('/stocks/intraday/<symbol>', methods = ['POST', 'GET'])
def intraday(symbol):
    function = 'TIME_SERIES_INTRADAY'
    json_dict = getResponse(symbol, function)

    openData = getOpen(symbol,json_dict)[::-1]
    closeData = getClose(symbol, json_dict)[::-1]
    date = getOpenDate(symbol, json_dict)[::-1]
    # maxOpen = getMax(openData)
    # minOpen = getMin(openData)
    # maxClose = getMax(closeData)
    # minClose = getMin(closeData)
    # maxOpen=maxOpen, minOpen=minOpen, maxClose=maxClose, minClose=minClose
    return render_template('intraday.html', openData=openData, closeData=closeData, symbol=symbol, date=date)

@app.route('/stocks/daily/<symbol>', methods = ['POST', 'GET'])
def daily(symbol):
    function = 'TIME_SERIES_DAILY'
    json_dict = getResponse(symbol, function)
    openData = getOpen(symbol,json_dict)[::-1]
    closeData = getClose(symbol, json_dict)[::-1]
    date = getOpenDate(symbol, json_dict)[::-1]
    # maxOpen = getMax(openData)
    # minOpen = getMin(openData)
    # maxClose = getMax(closeData)
    # minClose = getMin(closeData)
    # maxOpen = maxOpen, minOpen = minOpen, maxClose = maxClose, minClose = minClose
    return render_template('daily.html', openData=openData, closeData=closeData, symbol=symbol, date=date)

@app.route('/stocks/monthly/<symbol>', methods = ['POST', 'GET'])
def monthly(symbol):
    function = 'TIME_SERIES_MONTHLY'
    json_dict = getResponse(symbol, function)

    openData = getOpen(symbol,json_dict)[::-1]
    closeData = getClose(symbol, json_dict)[::-1]
    date = getOpenDate(symbol, json_dict)[::-1]
    # maxOpen = getMax(openData)
    # minOpen = getMin(openData)
    # maxClose = getMax(closeData)
    # minClose = getMin(closeData)
    # maxOpen=maxOpen, minOpen=minOpen, maxClose=maxClose, minClose=minClose
    return render_template('monthly.html', openData=openData, closeData=closeData, symbol=symbol, date=date)


def getResponse(symbol, function):
    API_KEY = 'O2877FVGMXZ33X94'
    API_URL = 'https://www.alphavantage.co/query'
    parameters = {
        'function': function,
        'symbol': symbol,
        'apikey': API_KEY
    }
    if function == 'TIME_SERIES_INTRADAY':
        parameters.update({'interval': '5min'})
        parameters.update({'outputsize': 'compact'})

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