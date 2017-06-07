import requests, json
from pprint import pprint

def getTiket(currency = 'ETH'):
	url = 'https://api.kraken.com/0/public/Ticker'
	currency = currency.upper()
	currency_pair = currency + 'EUR'
	currency_key = 'X' + currency + 'ZEUR'
	params = dict(pair=currency_pair)

	resp = requests.get(url=url, params=params)

	pprint(resp)
	data = json.loads(resp.text)
	pprint(data)

	current_price = data['result'][currency_key]['c'][0]
	current_volume = data['result'][currency_key]['c'][1]

	return currency_pair, current_price, current_volume


def get_trump():
    url = "https://api.whatdoestrumpthink.com/api/v1/quotes/random"
    resp = requests.get(url=url, params=dict())

    pprint(resp)
    data = json.loads(resp.text)
    pprint(data)
