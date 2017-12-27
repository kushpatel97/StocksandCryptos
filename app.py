from flask import Flask, render_template
import json
import requests

app = Flask(__name__)
@app.route('/daily/symbol/<symbol>')
def daily(symbol):
    API_KEY = 'O2877FVGMXZ33X94'
    API_URL = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    parmaters = {
        'function': function,
        'symbol': symbol,
        'apikey': API_KEY
    }
    json_data = requests.get(API_URL, params=parmaters)
    json_dict = json.loads(json_data.content)

    openData = getOpen(symbol,json_dict)
    closeData = getClose(symbol, json_dict)
    date = getOpenDate(symbol, json_dict)

    return render_template('index.html', openData=openData, closeData=closeData, symbol=symbol, date=date)

# def getResponse(symbol, function):
#     API_KEY = 'O2877FVGMXZ33X94'
#     API_URL = 'https://www.alphavantage.co/query'
#     parameters = {
#         'function': function,
#         'symbol': symbol,
#         'apikey': API_KEY
#     }
#     json_data = requests.get(API_URL, params=parameters)
#     json_dict = json.loads(json_data.content)
#     return json_dict

# Returns float array
def getOpen(symbol,json_dict):
    opened = []
    for key, val in json_dict['Time Series (Daily)'].items():
        opened.append(val['1. open'])
    return list(map(float,opened))

def getClose(symbol, json_dict):
    closed = []
    for key, val in json_dict['Time Series (Daily)'].items():
        closed.append(val['4. close'])
    return list(map(float,closed))
# Returns string array
def getOpenDate(symbol,json_dict):
    date = []
    for key in json_dict['Time Series (Daily)']:
        date.append(key)
    return date

if __name__ == '__main__':
    app.run(debug=True)