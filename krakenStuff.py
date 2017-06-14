import requests, json
from pprint import pprint


class Kraken:
    def __init__(self):
        self.assets = self.getAssets()

        self.assetNameKeys = {}
        for key, value in self.assets.iteritems():
            self.assetNameKeys[value['altname']] = key

    def getTiket(self, currency = 'ETH'):
    	url = 'https://api.kraken.com/0/public/Ticker'
    	currency = currency.upper()
    	currency_pair = currency + 'EUR'
    	currency_key = self.assetNameKeys[currency] + 'ZEUR'
    	params = dict(pair=currency_pair)

    	resp = requests.get(url=url, params=params)
    	data = json.loads(resp.text)
        if len(data["error"]) > 0:
            return "", -1, 0
    	current_price = data['result'][currency_key]['c'][0]
    	current_volume = data['result'][currency_key]['v'][1]

    	return currency_pair, float(current_price), float(current_volume)*float(current_price)

    def getAssets(self):
        url = 'https://api.kraken.com/0/public/Assets'
        resp = requests.get(url=url)
        data = json.loads(resp.text)
        return data['result']


def get_trump():
    url = "https://api.whatdoestrumpthink.com/api/v1/quotes/random"
    resp = requests.get(url=url, params=dict())

    pprint(resp)
    data = json.loads(resp.text)
    pprint(data)
    return data["message"]
