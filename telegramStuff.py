from krakenStuff import *

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import logging
import time
from collections import defaultdict

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

from functools import wraps
import pickle

class TelegramBot:

    def __init__(self, exchange):
        self.exchange = exchange
        self.admins = [42536066]

        # Create the EventHandler and pass it your bot's token.
        with open('telegramToken.txt', 'r') as f:
            self.telegramToken = f.readline().strip()
        self.updater = Updater(self.telegramToken)

        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        #Send init telegram message to Jesus
        self.dp.bot.send_message(chat_id=self.admins[0], text=u'\U0001F603' + "CriptonitoBot Bot Just Started!")

        # on different commands - answer in Telegram
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("help", self.help))

        self.dp.add_handler(CommandHandler("add", self.addAlert))
        self.dp.add_handler(CommandHandler("remove", self.removeAlert))
        self.dp.add_handler(CommandHandler("alerts", self.printAlerts))

        # on noncommand i.e message - Filter by Text (no photos or audios), and process the message
        self.dp.add_handler(MessageHandler(Filters.text, self.processMessage))

        # log all
        self.dp.add_error_handler(self.error)

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.start_polling()

        #self.updater.idle()
        try:
            self.profiles = pickle.load( open( "profiles.p", "rb" ) )
        except:
            print("problem loading profiles")
            self.profiles = mydefaultdict(UserProfile)

    def addAlert(self, bot, update):
        response = update.message.text.split(" ")
        chatId = update.message.chat["id"]
        userId = update.message.from_user["id"]
        #Checks
        if userId not in self.admins:
            update.message.reply_text("You are not an admin")
            return

        update.message.reply_text("Not implemented")
        return

        if len(response) != 3:
            return
        try:
            percentage = float(response[2])
        except ValueError:
            return
        
        coin = response[1]
        if exchange.getCoinInfo(coin) == None:
            print("Bad coin for " + coin + ". User " + str(chatId))
            update.message.reply_text(coin + " is not a valid coin")
            return

        coinInfo = self.exchange.getCoinInfo(coin)
        # /Checks

        self.profiles[chatId].alerts[coin] = Alert(coin, percentage)
        self.profiles[chatId].alerts[coin].SetLastPrice(coinInfo.price_usd)

        pickle.dump( self.profiles, open( "profiles.p", "wb" ) )
        print("New alert created for " + coin + ". User " + str(chatId))
        update.message.reply_text("I will alert you if " + coin + " changes by more than " + str(percentage) + "%")


    def removeAlert(self, bot, update):
        chatId = update.message.chat["id"]
        userId = update.message.from_user["id"]
        if userId not in self.admins:
            update.message.reply_text("You are not an admin")
            return
        
        update.message.reply_text("Not implemented")
        return

        try:
            response = update.message.text.split(" ")
            coin = response[1]
            self.profiles[chatId].alerts.pop(coin)
            pickle.dump( self.profiles, open( "profiles.p", "wb" ) )
            update.message.reply_text("Done!")
        except:
            update.message.reply_text("Problem removing")
            return

    def printAlerts(self, bot, update):

        update.message.reply_text("Not implemented")
        return

        chatId = update.message.chat["id"]
        response = "Alerts:\r\n"
        for key, value in self.profiles[chatId].alerts.iteritems():
            response+=key + " " + str(value.percentage) + "%\r\n"
        update.message.reply_text(response)

    def killBot(self):
        self.updater.stop()

    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    def start(self, bot, update):
        update.message.reply_text("Hi! I'm Criptonito Bot")

    def help(self, bot, update):
        response = '/add coin percentage\r\nPara agregar una alerta\r\n/remove coin\r\nPara eliminar una alerta\r\n'
        response+="I can show you prices for:\r\n"
        for key, value in self.exchange.assetPairs.iteritems():
            response += key + ", "
        update.message.reply_text(response)


    def processMessage(self, bot, update):
        message = update.message.text
        if message.upper() == "TRUMP":
            update.message.reply_text(get_trump())
        
        message = update.message.text
        message = update.message.text.split(" ")
        if len(message) != 2 or message[0].lower() != "get":
            return

        coin = message[1]
        if coin.upper() == "TRUMP":
            update.message.reply_text("Let's not get Trump here, shall we?")
            return

        coinInfo = self.exchange.getCoinInfo(coin)
        if coinInfo == None or "error" in coinInfo:
            update.message.reply_text("I'm no fool. That's not a coin")
            return
        coinInfo = coinInfo[0]
        update.message.reply_text("<code>Coin Name: " + coinInfo["name"] +
                                    "\r\nid: " + coinInfo["id"] +
                                    "\r\nSymbol: " + coinInfo["symbol"] +
                                    "\r\nPrice = " + str(round(coinInfo["price_eur"], 4)) + " " + u'\u20ac' +
                                    "\r\n24h Volume = " + str(round(coinInfo["24h_volume_usd"] / 1000000, 3)) + " M " + "USD" +
                                    "\r\n24h Change = " + str(coinInfo["percent_change_24h"]) + "%" + "</code>", parse_mode=ParseMode.HTML)
        
        print update.message.from_user.username, coinInfo
        return
        

    def error(self, bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))

    def sendMessage(self, id, msg):
        self.dp.bot.send_message(chat_id=id, text=msg)

class UserProfile:
    def __init__(self, chatId):
        self.chatId = chatId
        self.name = ""
        self.alerts = {}
        self.interests = []
        print("New profile created for " + str(self.chatId))


class Alert:
    def __init__(self, assetPair, percentage):
        self.assetPair = assetPair
        self.percentage = percentage
        self.lastPrice = 0
        self.maxTriggerPrice = 99999
        self.minTriggerPrice = -1


    def SetLastPrice(self, price):
        self.lastPrice = price
        self.maxTriggerPrice = self.lastPrice * (1 + (self.percentage / 100))
        self.minTriggerPrice = self.lastPrice * (1 - (self.percentage / 100))


class mydefaultdict(defaultdict):
    def __missing__(self, key):
        self[key] = new = self.default_factory(key)
        return new
