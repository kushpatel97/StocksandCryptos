import requests, json

API_KEY = 'O2877FVGMXZ33X94'
API_URL = 'https://www.alphavantage.co/query'
function = 'TIME_SERIES_DAILY'
symbol = 'AAPL'
interval = '60min'
parmaters = {
    'function': function,
    'symbol': symbol,
    # 'interval': interval,
    'apikey': API_KEY
}
res = requests.get(API_URL, params=parmaters)
json_dict = json.loads(res.content)
opened = []
for key in json_dict['Time Series (Daily)']:
    opened.append(key)
# opened = ','.join(opened)
print(opened)
