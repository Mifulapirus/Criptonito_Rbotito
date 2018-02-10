import requests, json
from pprint import pprint
import sys
from utils import *

class CoinMarketCap:
	def __init__(self):
		self.symbolIdDict = self.getsymbolIdDict()

	#Compile a list of coin ids from their symbol
	#So users can refer to the top 100 coins by their shorter symbol
	def getsymbolIdDict(self):
		ticker = self.getTicker()
		ids = {}
		for coin in ticker:
			ids[coin["symbol"]] = coin["id"]
		return ids
		
	def getIdList(self):
		ticker = self.getTicker()
		ids = []
		for coin in ticker:
			ids.append(coin["id"])
		return ids

	def getTicker(self, coinId = ""):
		url = "https://api.coinmarketcap.com/v1/ticker/"
		cId = coinId
		fullUrl = url + coinId + "/?convert=EUR"

		if coinId == "":
			fullUrl = "https://api.coinmarketcap.com/v1/ticker/?limit=0"
		resp = requests.get(url=fullUrl)
		try:
			data = json.loads(resp.text)
			return convertFromUnicode(data)
		except:
			e = sys.exc_info()[0]
			print "getTicker", e
			return None

	def getId(self, symbol):
		if symbol.upper() in self.symbolIdDict:
			coinId = self.symbolIdDict[symbol.upper()]
			return coinId
		return symbol
		
	def getCoinInfo(self, coin):
		coin = self.getId(coin)
		return self.getTicker(coin.lower())

if __name__ == "__main__":
	cmc = CoinMarketCap()
	print cmc.getCoinInfo("ethereum")