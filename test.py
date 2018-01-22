import requests, json, cryptos, app
from keys import API_URL, API_KEY
haveget = '2'.join(['BTC','USD'])
spl = haveget.split('2')
have = spl[0]
get = spl[1]

symbol = 'BTC'
market = 'KRW'

parameters = {
    'function': 'DIGITAL_CURRENCY_WEEKLY',
    'symbol': symbol,
    'market': market,
    'apikey': API_KEY
}
json_data = requests.get(API_URL, params=parameters)
json_dict = app.getMarketResponse(symbol, market)
# print(json_dict)
# fromcode = json_dict['Realtime Currency Exchange Rate']['1. From_Currency Code']
# fromname = json_dict['Realtime Currency Exchange Rate']['2. From_Currency Name']
# tocode = json_dict['Realtime Currency Exchange Rate']['3. To_Currency Code']
# toname = json_dict['Realtime Currency Exchange Rate']['4. To_Currency Name']
# exchange = json_dict['Realtime Currency Exchange Rate']['5. Exchange Rate']

curr1 = 'USD'
curr2 = 'KRW'
exc = app.exchangeRate(app.getConversionRes(curr1, curr2))
print('1 ' + curr1 + ' equals ' + exc +' '+curr2)
exc = float(exc)

for key in json_dict:
    timeseries = key
dates = []
close = []
usd = []
for key, val in json_dict[timeseries].items():
    dates.append(key)
    close.append(val['4a. close ('+curr2+')'])
    usd.append(val['4b. close (' + curr1 + ')'])
close = list(map(float, close))
usd = list(map(float,usd))
converted =[x/exc for x in close]
print('Dates: ')
print(dates)
print(curr2 +  ' Close: ')
print(close)
print('KRW --> USD: ')
print(converted)
print('USD BTC: ')
print(usd)