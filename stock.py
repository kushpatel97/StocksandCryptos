class Stock:
    def __init__(self, symbol, json_dict):
        self.symbol = symbol
        self.json_dict = json_dict

    # Returns float array
    def getOpen(symbol, json_dict):
        for key in json_dict:
            timeseries = key
        opened = []
        for key, val in json_dict[timeseries].items():
            opened.append(val['1. open'])
        return list(map(float, opened))

    def getClose(symbol, json_dict):
        for key in json_dict:
            timeseries = key
        closed = []
        for key, val in json_dict[timeseries].items():
            closed.append(val['4. close'])
        return list(map(float, closed))

    # Returns string array
    def getOpenDate(symbol, json_dict):
        for key in json_dict:
            timeseries = key
        date = []
        for key in json_dict[timeseries]:
            date.append(key)
        return date