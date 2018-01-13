from keys import API_KEY, API_URL
import json, requests


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
