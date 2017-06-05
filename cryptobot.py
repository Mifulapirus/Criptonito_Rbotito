"""
 Title: Criptobot
 Description: You ask about a price and it just answers
""" 
__author__ = "Angel Hernandez"
__contributors__ = "Angel Hernandez"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Angel Hernandez"
__email__ = "angel@tupperbot.com"
__status__ = "beta"

import time
import requests, json
from pprint import pprint
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop


token = '346851548:AAGCYjc8FtxGbjlTMeVvfaqPoPb8bWMWsUY'


def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	pprint(msg)
	currency = msg['text'].replace('@criptonito_bot ', "")
	currency_pair, current_price, current_volume = getTiket(currency)
	telegram_send(chat_id, 	"Pair: " + currency_pair + 
							"\r\nEUR = " + str(current_price) + 
							"\r\nVolume = " + str(current_volume))

def telegram_send(chat_id, text, markup = ""):
	print "Sending message to " + str(chat_id)
	print text
	try:
		bot.sendMessage(chat_id, text, reply_markup=markup)
		return True

	except Exception as err:
		print "ERROR sending telegram message: "
		print err
		return False


def getTiket(currency = 'ETH'):
	url = 'https://api.kraken.com/0/public/Ticker'
	currency = currency.upper()
	currency_pair = currency + 'EUR'
	currency_key = 'X' + currency + 'ZEUR'
	params = dict(
	    pair=currency_pair)

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

if __name__ == '__main__':
	print "-------------------------------"
	print "|     Criptonito_bot 1.0      |"
	print "-------------------------------"
	#get_trump()
	try:
		bot = telepot.Bot(token)
		MessageLoop(bot, on_chat_message).run_as_thread()
		while True:
			time.sleep(10)

	except KeyboardInterrupt:
		print "CriptonitoBot is sad and letting you go... :("
		sys.exit()