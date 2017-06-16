from krakenStuff import *

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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
        self.dp.bot.send_message(chat_id=42536066, text=u'\U0001F603' + "CriptonitoBot Bot Just Started!")

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
        if len(response) != 3:
            return
        try:
            percentage = float(response[2])
        except ValueError:
            return
        asset = response[1].upper()
        if asset not in self.exchange.assetNameKeys:
            return

        currency_pair, current_price, current_volume = self.exchange.getTiket(asset)
        if current_price == 0:
            print("Bad coin for " + asset + ". User " + str(chatId))
            update.message.reply_text("Bad coin")
            return
        # /Checks

        self.profiles[chatId].alerts[asset] = Alert(asset, percentage)
        self.profiles[chatId].alerts[asset].SetLastPrice(current_price)

        pickle.dump( self.profiles, open( "profiles.p", "wb" ) )
        print("New alert created for " + asset + ". User " + str(chatId))
        update.message.reply_text("I will alert you if " + asset + " changes by more than " + str(percentage) + "%")


    def removeAlert(self, bot, update):
        chatId = update.message.chat["id"]
        userId = update.message.from_user["id"]
        if userId not in self.admins:
            update.message.reply_text("You are not an admin")
            return
        try:
            response = update.message.text.split(" ")
            self.profiles[chatId].alerts.pop(response[1].upper())
            pickle.dump( self.profiles, open( "profiles.p", "wb" ) )
            update.message.reply_text("Done!")
        except:
            update.message.reply_text("Problem removing")
            return

    def printAlerts(self, bot, update):
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
        for key, value in self.exchange.assetNameKeys.iteritems():
            response += key + ", "
        update.message.reply_text( + response)

    def processMessage(self, bot, update):
        message = update.message.text

        if message.upper() in self.exchange.assetNameKeys:
            currency_pair, current_price, current_volume = self.exchange.getTiket(message)

            update.message.reply_text("Pair: " + currency_pair +
                                    "\r\nPrice = " + str(round(current_price, 4)) + " " + u'\u20ac' +
                                    "\r\nVolume = " + str(round(current_volume / 1000000, 3)) + " M" + u'\u20ac')
            print update.message.from_user.username, currency_pair, current_price, current_volume
        if message.upper() == "TRUMP":
            update.message.reply_text(get_trump())

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
    def __init__(self, name, percentage):
        self.name = name
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
