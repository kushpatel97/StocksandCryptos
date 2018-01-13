from flask import Flask, render_template, url_for, redirect, request
from keys import API_KEY, API_URL
import cryptos
import json
import requests
import stock

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/checkcrypto', methods = ['POST', 'GET'])
def checkcrypto():
    if request.method == 'POST':
        have = request.form['have']
        get = request.form['get']
    return redirect(url_for('convert', have = have, get=get))

@app.route('/cryptos/convert/<have>', methods = ['POST', 'GET'])
def convert(have, get):
    res = cryptos.getConversionRes(have,get)
    codeFrom = cryptos.getFromCode(res)
    nameFrom = cryptos.getFromName(res)
    codeTo = cryptos.getToCode(res)
    nameTo = cryptos.getToName(res)
    exchangeRates = cryptos.exchangeRate(res)
    render_template('conversion.html', have = have, get = get, codeFrom = codeFrom, nameFrom = nameFrom, codeTo = codeTo, nameTo = nameTo, exchangeRates = exchangeRates)

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

    json_data = requests.get(API_URL, params=parameters)
    json_dict = json.loads(json_data.content)
    return json_dict


if __name__ == '__main__':
    app.run(debug=True)