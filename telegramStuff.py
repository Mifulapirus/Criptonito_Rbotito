from krakenStuff import *

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, exchange):
        self.exchange = exchange

        # Create the EventHandler and pass it your bot's token.
        with open('telegramToken.txt', 'r') as f:
            self.telegramToken = f.readline().strip()
        self.updater = Updater(self.telegramToken)

        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        #Send init telegram message to Jesus
        self.dp.bot.send_message(chat_id=42536066, text="CriptonitoBot Bot Just Started!")

        # on different commands - answer in Telegram
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("help", self.help))

        # on noncommand i.e message - Filter by Text (no photos or audios), and process the message
        self.dp.add_handler(MessageHandler(Filters.text, self.processMessage))

        # log all
        self.dp.add_error_handler(self.error)

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.start_polling()

        #self.updater.idle()

    def killBot(self):
        self.updater.stop()

    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    def start(self, bot, update):
        update.message.reply_text("Hi! I'm Criptonito Bot")

    def help(self, bot, update):
        update.message.reply_text('Help? I can barely help myself')

    def processMessage(self, bot, update):
        message = update.message.text

        if message.upper() in self.exchange.assetNameKeys:
            currency_pair, current_price, current_volume = self.exchange.getTiket(message)
            update.message.reply_text("Pair: " + currency_pair +
                                    "\r\nEUR = " + str(current_price) +
                                    "\r\nVolume = " + str(current_volume))
        else:
            print message, "Not an asset"


    def error(self, bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))
