import requests, json

API_KEY = 'O2877FVGMXZ33X94'
API_URL = 'https://www.alphavantage.co/query'
function = 'TIME_SERIES_INTRADAY'
symbol = 'AAPL'
interval = '5min'
parmaters = {
    'function': function,
    'symbol': symbol,
    'interval': interval,
    'outputsize': 'compact',
    'apikey': API_KEY
}
res = requests.get(API_URL, params=parmaters)
json_dict = json.loads(res.content)
for key in json_dict:
    ans = key
print(key)
# opened = []
# for key in json_dict['Time Series (Daily)']:
#     opened.append(key)
# # opened = ','.join(opened)
# print(opened)
