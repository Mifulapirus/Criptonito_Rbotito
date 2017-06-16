import requests, json
from pprint import pprint


class Kraken:
	def __init__(self):
		self.assets = self.getAssets()
		self.assetPairs = self.getAssetPairs()


	def getPair(self, asset, currency = 'EUR'):
		asset = asset.upper()
		pairName = asset + currency
		pair = 'X' + asset + 'Z' + currency
		if pair in self.assetPairs:
			return pair
		else:
			return None

	def getTiket(self, assetPair):
		url = 'https://api.kraken.com/0/public/Ticker'
		params = dict(pair=assetPair)

		resp = requests.get(url=url, params=params)
		try:
			data = json.loads(resp.text)
			if len(data["error"]) > 0:
				return "", -1, 0
			current_price = data['result'][assetPair]['c'][0]
			current_volume = data['result'][assetPair]['v'][1]

			return float(current_price), float(current_volume)*float(current_price)
		except:
			return -1, 0

	def getAssets(self):
		url = 'https://api.kraken.com/0/public/Assets'
		resp = requests.get(url=url)
		data = json.loads(resp.text)
		return data['result']

	def getAssetPairs(self):
		url = 'https://api.kraken.com/0/public/AssetPairs'
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
