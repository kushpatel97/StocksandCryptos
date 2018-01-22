from flask import Flask, render_template, url_for, redirect, request
from keys import API_KEY, API_URL
import json, requests
import stock, cryptos

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/checkcrypto', methods = ['POST'])
def checkcrypto():
    if request.method == 'POST':
        have = request.form['have']
        get = request.form['get']
        haveget = '2'.join([have,get])
        return redirect(url_for('convert', haveget=haveget))
    return redirect(url_for('convert', haveget = None))

@app.route('/checkmarket', methods = ['POST'])
def checkmarket():
    if request.method == 'POST':
        symbol = request.form['symbol']
        market = request.form['market']
        symbolmarket = '+'.join([symbol,market])
        return redirect(url_for('market', symbolmarket=symbolmarket))
    return redirect(url_for('market', symbolmarket = None))

@app.route('/checkcomparisons', methods = ['POST','GET'])
def checkcomparisons():
    if request.method == 'POST':
        cryptocurrency = request.form['cryptocurrency']
        market1 = request.form['market1']
        market2 = request.form['market2']
        results = '+'.join([cryptocurrency,market1,market2])
        return redirect(url_for('comparisons', results = results))
    return redirect(url_for('comparisons'), results = None)

@app.route('/cryptos/comparisons/<results>', methods = ['POST', 'GET'])
def comparisons(results):
    arr = results.split('+')
    crypto = arr[0]
    market1 = arr[1]
    market2 = arr[2]
    date = []
    market1_sym = []
    market2_sym = []
    exchange_rate = float(exchangeRate(getConversionRes(market1,market2)))
    response = getMarketResponse(crypto, market2)
    timeseries = getTimeseries(response)
    for key, val in response[timeseries].items():
        date.append(key)
        market2_sym.append(val['4a. close ('+market2+')'])
        market1_sym.append(val['4b. close ('+market1+')'])

    market2_sym = list(map(float, market2_sym))
    market1_sym = list(map(float, market1_sym))
    mk2exc = [x/exchange_rate for x in market2_sym]
    date = reversed(date)
    market1_sym = market1_sym[::-1]
    mk2exc = mk2exc[::-1]

    exchange_rate = float(exchangeRate(getConversionRes(market1,market2)))

    return render_template('JMZ.html', exchange_rate = exchange_rate, date=date, market1_sym=market1_sym, mk2exc=mk2exc)

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
        'function': 'DIGITAL_CURRENCY_WEEKLY',
        'symbol': symbol,
        'market': market,
        'apikey': API_KEY
    }
    json_data = requests.get(API_URL, params=parameters)
    json_dict = json.loads(json_data.content)
    return json_dict

#  Crypto Currency Methods
def getTimeseries(json_dict):
    for key in json_dict:
        timeseries = key
    return timeseries
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