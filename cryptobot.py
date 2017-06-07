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

from krakenStuff import *

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text("Hi! I'm Criptonito Bot")

def help(bot, update):
    update.message.reply_text('Help? I can barely help myself')

def processMessage(bot, update):
    print(update.message.text)
    currency_pair, current_price, current_volume = getTiket(update.message.text)

    update.message.reply_text("Pair: " + currency_pair +
                            "\r\nEUR = " + str(current_price) +
                            "\r\nVolume = " + str(current_volume))

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    print "-------------------------------"
    print "|     Criptonito_bot 1.0      |"
    print "-------------------------------"

    # Create the EventHandler and pass it your bot's token.
    with open('telegramToken.txt', 'r') as f:
        telegramToken = f.readline().strip()
    updater = Updater(telegramToken)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    #Send telegram message to Jesus
    dp.bot.send_message(chat_id=42536066, text="CriptonitoBot Bot Just Started!")

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - Filter by Text (no photos or audios), and process the message
    dp.add_handler(MessageHandler(Filters.text, processMessage))

    # log all
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()




    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    try:
        while True:
            #Here we can do other stuff, like periodically check for prices in order to send alerts
            time.sleep(10)
    except KeyboardInterrupt:
        print("CriptonitoBot is sad and letting you go... :(")
        print("Press Ctrl-C once more to kill me")

    updater.idle()


if __name__ == '__main__':
    main()
