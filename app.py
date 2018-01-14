from flask import Flask, render_template, url_for, redirect, request
from keys import API_KEY, API_URL
import json, requests
import stock, cryptos

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/checkcrypto', methods = ['POST', 'GET'])
def checkcrypto():
    if request.method == 'POST':
        have = request.form['have']
        get = request.form['get']
        haveget = '2'.join([have,get])
        return redirect(url_for('convert', haveget=haveget))
    return redirect(url_for('convert', haveget = None))

@app.route('/checkmarket', methods = ['POST', 'GET'])
def checkmarket():
    if request.method == 'POST':
        symbol = request.form['symbol']
        market = request.form['market']
        symbolmarket = '+'.join([symbol,market])
        return redirect(url_for('market', symbolmarket=symbolmarket))
    return redirect(url_for('market', symbolmarket = None))

@app.route('/cryptos/market/<symbolmarket>', methods = ['POST', 'GET'])
def market(symbolmarket):
    spl = symbolmarket.split('+')
    res = getMarketResponse(spl[0],spl[1])
    return render_template('cryptographs.html', symbol = spl[0], market = spl[1])

@app.route('/cryptos/convert/<haveget>', methods = ['POST', 'GET'])
def convert(haveget):
    spl = haveget.split('2')
    res = getConversionRes(spl[0],spl[1])
    nameFrom = getFromName(res)
    nameTo = getToName(res)
    exchangeRates = exchangeRate(res)
    return render_template('conversion.html', nameFrom = nameFrom, nameTo = nameTo, exchangeRates = exchangeRates)

@app.route('/checkstk',methods = ['POST', 'GET'])
def checkstk():
    if request.method == 'POST':
        stock = request.form['stock']
        return redirect(url_for('daily', symbol = stock))
    else:
        stock = request.args.get('stock')
        return redirect(url_for('daily', symbol = stock))
#  =====================================================================================================================
@app.route('/stocks', methods = ['POST', 'GET'])
def stocks():
    stock_symbols = stock.getStockSymbols()
    stock_name = stock.getStockName()
    zipped = list(zip(stock_symbols, stock_name))
    return render_template('stocks.html', stock_symbols = stock_symbols, stock_name = stock_name, zipped=zipped)

@app.route('/cryptos', methods = ['POST', 'GET'])
def cryptos():
    return render_template('cryptos.html')

@app.route('/stocks/intraday/<symbol>', methods = ['POST', 'GET'])
def intraday(symbol):
    function = 'TIME_SERIES_INTRADAY'
    json_dict = getResponse(symbol, function)
    temp = stock.Stock(symbol, json_dict)
    openData = temp.getOpen(symbol,json_dict)[::-1]
    closeData = temp.getClose(symbol, json_dict)[::-1]
    date = temp.getOpenDate(symbol, json_dict)[::-1]
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
    temp = stock.Stock(symbol, json_dict)
    openData = temp.getOpen(symbol,json_dict)[::-1]
    closeData = temp.getClose(symbol, json_dict)[::-1]
    date = temp.getOpenDate(symbol, json_dict)[::-1]
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
    temp = stock.Stock(symbol, json_dict)
    openData = temp.getOpen(symbol,json_dict)[::-1]
    closeData = temp.getClose(symbol, json_dict)[::-1]
    date = temp.getOpenDate(symbol, json_dict)[::-1]
    # maxOpen = getMax(openData)
    # minOpen = getMin(openData)
    # maxClose = getMax(closeData)
    # minClose = getMin(closeData)
    # maxOpen=maxOpen, minOpen=minOpen, maxClose=maxClose, minClose=minClose
    return render_template('monthly.html', openData=openData, closeData=closeData, symbol=symbol, date=date)

#  =====================================================================================================================

def getResponse(symbol, function):
    parameters = {
        'function': function,
        'symbol': symbol,
        'apikey': API_KEY
    }
    if function == 'TIME_SERIES_INTRADAY':
        parameters.update({'interval': '5min'})
        parameters.update({'outputsize': 'compact'})

    if function == 'TIME_SERIES_DAILY':
        parameters.update({'outputsize': 'compact'})

    json_data = requests.get(API_URL, params=parameters)
    json_dict = json.loads(json_data.content)
    return json_dict

def getConversionRes(have, get):
    parameters = {
        'function': 'CURRENCY_EXCHANGE_RATE',
        'from_currency': have,
        'to_currency': get,
        'apikey': API_KEY
    }
    json_data = requests.get(API_URL, params=parameters)
    json_dict = json.loads(json_data.content)
    return json_dict


def getMarketResponse(symbol, market):
    parameters = {
        'function': 'DIGITAL_CURRENCY_INTRADAY',
        'symbol': symbol,
        'market': market,
        'apikey': API_KEY
    }
    json_data = requests.get(API_URL, params=parameters)
    json_dict = json.loads(json_data.content)
    return json_dict

#  Crypto Currency Methods


def getFromCode(json_dict):
    return json_dict['Realtime Currency Exchange Rate']['1. From_Currency Code']

def getFromName(json_dict):
    return json_dict['Realtime Currency Exchange Rate']['2. From_Currency Name']

def getToCode(json_dict):
    return json_dict['Realtime Currency Exchange Rate']['3. To_Currency Code']

def getToName(json_dict):
    return json_dict['Realtime Currency Exchange Rate']['4. To_Currency Name']

def exchangeRate(json_dict):
    return json_dict['Realtime Currency Exchange Rate']['5. Exchange Rate']

if __name__ == '__main__':
    app.run(debug=True)