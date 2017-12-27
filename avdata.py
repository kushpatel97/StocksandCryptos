import requests, json
API_KEY = 'O2877FVGMXZ33X94'
API_URL = 'https://www.alphavantage.co/query'

class Intraday():
    MIN1_INTERVAL   = '1min'
    MIN5_INTERVAL   = '5min'
    MIN15_INTERVAL  = '15min'
    MIN30_INTERVAL  = '30min'
    MIN60_INTERVAL  = '60min'
    COMPACT_OUTPUT  = 'compact'
    FULL_OUTPUT     = 'full'

class alphavantage():

    def __init__(self, symbol):
        self.API_KEY = API_KEY
        self.API_URL = API_URL
        self.symbol = symbol

    def Intraday(self,interval):
        parmaters = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': self.symbol,
            'interval': interval,
            'apikey': API_KEY
        }
        res = requests.get(API_URL,params=parmaters)
        json_data = res.content
        json_dict = json.loads(json_data)
        return json_dict