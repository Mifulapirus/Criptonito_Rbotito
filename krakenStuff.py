import requests, json
from pprint import pprint
import sys

class Kraken:
	def __init__(self):
		self.assetPairs = self.getAssetPairs()

	def getPair(self, asset, currency = 'EUR'):
		asset = asset.upper()
		currency = currency.upper()
		pair = 'X' + asset + 'Z' + currency
		if pair in self.assetPairs:
			return pair
		else:
			return None

	def getTiker(self, assetPair):
		url = 'https://api.kraken.com/0/public/Ticker'
		params = dict(pair=assetPair)

		resp = requests.get(url=url, params=params)
		try:
			data = json.loads(resp.text)
			if len(data["error"]) > 0:
				return "", -1, 0

			#myTicker = Ticker(assetPair, data['result'][assetPair])

			current_price = data['result'][assetPair]['c'][0]
			current_volume = data['result'][assetPair]['v'][1]

			return float(current_price), float(current_volume)*float(current_price)
		except:
			e = sys.exc_info()[0]
			print "getTicker", e
			return -1, 0

	def getAssetPairs(self):
		url = 'https://api.kraken.com/0/public/AssetPairs'
		resp = requests.get(url=url)
		data = json.loads(resp.text)
		return data['result']

class Ticker:
	def __init__(self, pair, result):
		self.pair = pair
		#print "New Ticker", pair
		self.ask = AskBidArray(result['a'])
		self.bid = AskBidArray(result['b'])
		self.lastTradeClosed = L24HArray(result['c'])
		self.volume = L24HArray(result['v'])
		self.volumeWeightedAverage = L24HArray(result['p'])
		self.numberOfTrades = L24HArray(result['t'])
		self.low = L24HArray(result['l'])
		self.high = L24HArray(result['h'])
		self.todaysOpeningPrice = float(result['o'])

class AskBidArray:
	def __init__(self, array):
		self.price = float(array[0])
		self.wholeLotVolume = float(array[1])
		self.lotVolume = float(array[2])
		#print "New AskBidArray", self.price, self.wholeLotVolume, self.lotVolume

class L24HArray:
	def __init__(self, array):
		self.today = float(array[0])
		self.last24Hours = float(array[1])
		#print "New L24H Array", self.today, self.last24Hours

def get_trump():
	url = "https://api.whatdoestrumpthink.com/api/v1/quotes/random"
	resp = requests.get(url=url, params=dict())

	pprint(resp)
	data = json.loads(resp.text)
	pprint(data)
	return data["message"]
