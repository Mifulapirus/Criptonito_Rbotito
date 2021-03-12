import requests
import json

class Binance:
    def __init__(self):
        self._baseURL = "https://api.binance.com"
        self.availablePairs = []

        self.updateAvailablePairs()
                
    def updateAvailablePairs(self):
        symbols = self._resquest("/api/v3/exchangeInfo")['symbols']
        for pair in symbols:
            self.availablePairs.append({'pair':pair['symbol'], 'baseAsset':pair['baseAsset'], 'quoteAsset':pair['quoteAsset']})
    
    def checkIfPairExists(self, pair):
        if any(tempDict['pair'] == pair for tempDict in self.availablePairs):
            return True
        else:
            return False

    def checkIfBaseAsset(self, baseAsset):
        if any(tempDict['baseAsset'] == baseAsset for tempDict in self.availablePairs):
            return True
        else:
            return False

    def getPrice(self, pair):
        if self.checkIfPairExists(pair):
            result = []
            result.append(self._resquest("/api/v3/ticker/price",  params={'symbol': pair})['price'])
            result.append(self.getBaseAsset(pair))
            result.append(self.getQuoteAsset(pair))
            return result

        return -1

    def getPriceSimple(self, pair):
        return self.getPrice(pair)[0]
        
    def getBaseAsset(self, pair):
        if self.checkIfPairExists(pair):
            pairInfo = next(item for item in self.availablePairs if item['pair'] == pair)
            return pairInfo['baseAsset']

        else: return -1

    def getQuoteAsset(self, pair):
        if self.checkIfPairExists(pair):
            pairInfo = next(item for item in self.availablePairs if item['pair'] == pair)
            return pairInfo['quoteAsset']

        else: return -1
    
    def _resquest(self, endpoint, params=""):
        """Makes a request to binance"""
        resp = requests.get(self._baseURL + endpoint, params)
        if resp.status_code != 200:
            # This means something went wrong.
            print("GET " + endpoint + ': {}'.format(resp.status_code))
            return resp.status_code

        else:
            return resp.json()

    

    
if __name__ == "__main__":
    binance = Binance()
    #print (binance.checkIfPairExists('ETHBTC'))
    #print (binance.checkIfPairExists('ETHBTG'))
    for i in range(15):
        print(binance.getPrice("ETHBTC"))
        print(binance.getPriceSimple("ETHBTC"))
    #print (binance.getBaseAsset("ETHBTG"))
"""


def request(endpoint):


def getServerTime():
    resp = request("/api/v3/time")
    print(resp)
    
    

def ping():
    print(request("/api/v3/ping"))

def getAvailablePairs():
    availablePairs = request("/api/v3/exchangeInfo")
    for symbol in resp['symbols']:
        if(symbol['baseAsset'] == 'XLM'):
            print(symbol['symbol'])

getAvailablePairs()
"""