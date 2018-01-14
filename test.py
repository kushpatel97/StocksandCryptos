import requests, json, cryptos, app
from keys import API_URL, API_KEY
haveget = '2'.join(['BTC','USD'])
spl = haveget.split('2')
have = spl[0]
get = spl[1]

symbol = 'BTC'
market = 'KRW'

parameters = {
    'function': 'DIGITAL_CURRENCY_INTRADAY',
    'symbol': symbol,
    'market': market,
    'apikey': API_KEY
}
json_data = requests.get(API_URL, params=parameters)
json_dict = json.loads(json_data.content)

# fromcode = json_dict['Realtime Currency Exchange Rate']['1. From_Currency Code']
# fromname = json_dict['Realtime Currency Exchange Rate']['2. From_Currency Name']
# tocode = json_dict['Realtime Currency Exchange Rate']['3. To_Currency Code']
# toname = json_dict['Realtime Currency Exchange Rate']['4. To_Currency Name']
# exchange = json_dict['Realtime Currency Exchange Rate']['5. Exchange Rate']

# print(cryptos.getToName(json_dict))

# print(zip(fromcode, fromname, tocode, toname, exchange))

res = app.getMarketResponse(symbol,market)

for item in res:
    timeseries = item


for key, val in res[timeseries].items():
    print(val)
