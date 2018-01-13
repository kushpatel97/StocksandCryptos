import requests, json
from keys import API_URL, API_KEY

parameters = {
    'function': 'CURRENCY_EXCHANGE_RATE',
    'from_currency': 'XRP',
    'to_currency': 'USD',
    'apikey': API_KEY
}
json_data = requests.get(API_URL, params=parameters)
json_dict = json.loads(json_data.content)

fromcode = json_dict['Realtime Currency Exchange Rate']['1. From_Currency Code']
fromname = json_dict['Realtime Currency Exchange Rate']['2. From_Currency Name']
tocode = json_dict['Realtime Currency Exchange Rate']['3. To_Currency Code']
toname = json_dict['Realtime Currency Exchange Rate']['4. To_Currency Name']
exchange = json_dict['Realtime Currency Exchange Rate']['5. Exchange Rate']

print(zip(fromcode, fromname, tocode, toname, exchange))
