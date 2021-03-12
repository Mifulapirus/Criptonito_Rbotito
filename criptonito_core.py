#!/usr/bin/env py
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
 Title: CriptoBot
 Description: You ask about a price and it just answers
"""
__author__ = "Angel Hernandez, Jesus Dominguez"
__contributors__ = "Angel Hernandez, Jesus Dominguez"
__license__ = "GPL"
__version__ = "0.2"
__maintainer__ = "Angel Hernandez, Jesus Dominguez"
__email__ = "angel@gaubit.com, jcobreros@gmail.com"
__status__ = "beta"


import logging
from datetime import datetime
import os.path
import sys

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, Handler, CallbackContext
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from configparser import ConfigParser
import traceback
import html
import json

import binance


#Default Paths
ownName = os.path.basename(__file__)
ownPath = sys.argv[0].replace('\\' + ownName, '')
logsPath = ownPath + "//logs"
ownLogPath = logsPath + "/criptonito.log"
configurationPath = ownPath + "//config.ini"

# read configuration
config = ConfigParser()
print(ownPath)
config.read(configurationPath, "utf8")
timeout = int(config.get("telegram", "timeout"))
owner_id = str(config.get("telegram", "owner_id"))

# Set up logging to a file and on screen
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(ownLogPath) #TODO Make sure this folder exists before doing this
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

#Binance
binance = binance.Binance()

#Conversation Steps
BEGIN, PAIR, PRICE, DIRECTION = range(4)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Log the begining of a new conversation"""
    user = update.message.from_user
    logger.info("Conversation started with %s",  user.first_name)
    update.message.reply_text('👋 ' + user.first_name + " I'm here to help you getting information about all cryptocurrencies I know")
def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
def checkForPair(update, context):
    """Echo the user message."""
    text = update.message.text.upper()    
    for word in text.split():
        print("Checking for pair on text: " + word)
        if binance.checkIfPairExists(word):
            logger.info("Pair detected " + word)
            pairInfo = binance.getPrice(word)
            msg =       "*" + word + "*\n"
            msg = msg + "   1 " + pairInfo[1] + " = " + pairInfo[0] + " " + pairInfo[2]
            update.message.reply_text(msg,  parse_mode=ParseMode.MARKDOWN)

        print("Checking Base Assets for: " + word)
        if binance.checkIfBaseAsset(word):
            logger.info("Base Asset Detected " + word)
            #provide USD and BTC pairs
            msg =""
            if binance.checkIfPairExists(word + "BTC"):
                btcPair = word + "BTC"
                logger.info("BTC pair detected " + btcPair)
                pairInfo = binance.getPrice(btcPair)
                msg += "   1 " + pairInfo[1] + " = " + pairInfo[0] + " " + pairInfo[2] + "\n"
            if binance.checkIfPairExists(word + "USDT"):
                usdtPair = word + "USDT"
                logger.info("USDT pair detected " + usdtPair)
                pairInfo = binance.getPrice(usdtPair)
                msg += "1 " + pairInfo[1] + " = " + pairInfo[0] + " " + pairInfo[2]
            
            update.message.reply_text(msg,  parse_mode=ParseMode.MARKDOWN)


        
#Alert Conversation handlers
def alertAdd(update, context):
    user = update.message.from_user
    if context.args:
        logger.info("Add Alert for %s with the following Arguments:", user.first_name)
        i=0
        for arg in context.args:
            logger.info(str(i) + " -> " + str(arg))
            i=i+1
        #Check if we got the right number of arguments
        if len(context.args) != 3:
            update.message.reply_text("Seems like you sent me " + str(len(context.args) + 
                "\nPlease send me the alert information as _/addAlert PAIR price above/below_" + 
                "\nFor example: _/addAlert XRPBTC 0.00003 above_", parse_mode=ParseMode.MARKDOWN))
            return BEGIN


    logger.info("Add Alert for %s", user.first_name)
    
    context.user_data['timestamp'] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    context.user_data['first_name'] = user.first_name
    context.user_data['last_name'] = user.last_name
    context.user_data['user_id'] = user.id
    context.user_data['user_name'] = user.username
    
    update.message.reply_text(
        "Wanna add an alert, huh? ok, let's do this!"
        "   First, send me the pair you are interested in, for example ETHBTC"
        "   You can also send /cancel to stop setting this alarm.\n\n", parse_mode=ParseMode.MARKDOWN)
    return PAIR
def alertPair(update, context):
    user = update.message.from_user
    pairText = update.message.text.upper()
    logger.info("   Alert for %s on the pair %s", user.first_name, pairText)

    if binance.checkIfPairExists(pairText):
        context.user_data['pair'] = pairText
        pairInfo = binance.getPrice(context.user_data['pair'])

        update.message.reply_text("Got it, Let's get you an alert for " + pairText + 
            "\n 1 " + pairInfo[1] + " 🔁 " + pairInfo[0] + " " + pairInfo[2] +
            "\n\n💰 Now tell me what *price* shall I set the alert to.\n" + 
            " For example: 0.024601", parse_mode =ParseMode.MARKDOWN)
        return PRICE
    else:
        update.message.reply_text("Sorry, I can't find " + pairText + " in Binance. Are you sure you spelled it right?", parse_mode = ParseMode.MARKDOWN)
        return PAIR     
def alertPrice(update, context):
    user = update.message.from_user
    logger.info("   Alert price for %s on the pair %s with price %s", user.first_name, context.user_data['pair'], update.message.text)

    try:
        pairPrice = float(update.message.text)
        context.user_data['price'] = pairPrice
        reply_keyboard = [['Above', 'Below']]
        update.message.reply_text("Ok, so do you want to get an alert when " + 
            context.user_data['pair'] + " goes *above* or *below* " +
            str(context.user_data['price']), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DIRECTION

    except:
        update.message.reply_text("I don't think " + update.message.text + " is a number.\nPlease give me a number like 2.4601")
        return PRICE 
def alertDirection(update, context):
    user = update.message.from_user
    logger.info("   Alert price for %s on the pair %s @ %s when it goes %s", user.first_name, context.user_data['pair'], context.user_data['price'], update.message.text)

    if any(ans in update.message.text for ans in ("Above", "above")): 
        context.user_data['direction'] = "above"
        logger.info("Alert is valid")
        return setAlert(update, context)

    elif any(ans in update.message.text for ans in ("Below", "below")):
        context.user_data['direction'] = "below"
        logger.info("Alert is valid")
        return setAlert(update, context)

    else:
        reply_keyboard = [['Above', 'Below']]
        update.message.reply_text("Wait, that's not any of the options I gave you. Please use one of the following options:", 
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DIRECTION

def setAlert(update, context):
    logger.info("New alert set:" +
                    "\n  Time: " + context.user_data['timestamp'] + 
                    "\n  User's Name: " + context.user_data['first_name'] + 
                    "\n  User's ID: " + str(context.user_data['user_id']) + 
                    "\n  Pair: " + context.user_data['pair'] +
                    "\n  Price: " + str(context.user_data['price']) +
                    "\n  Direction: " + context.user_data['direction'])

    update.message.reply_text("✅ Here is your alert information:" + 
                    "\n  *Time:* " + context.user_data['timestamp'] + 
                    "\n  *User's Name:* " + context.user_data['first_name'] + 
                    "\n  *Pair:* " + context.user_data['pair'] +
                    "\n  *Price:* " + str(context.user_data['price']) +
                    "\n  *Direction:* " + context.user_data['direction'], 
                    reply_markup=ReplyKeyboardRemove(), 
                    parse_mode = ParseMode.MARKDOWN)

    with open('alerts.json', 'a') as outfile:
        json.dump(context.user_data, outfile)
        outfile.write("\n")
    
    context.job_queue.run_repeating(checkAlert, interval=5, first=0, context = context)
    

    return ConversationHandler.END

def checkAlert(context: CallbackContext):
    logger.info("Checking alert: ")
    userData = context.job.context.user_data 
    currentPrice = float(binance.getPriceSimple(userData['pair']))
    print(currentPrice)
    if currentPrice < float(userData['price']):
        if (userData['direction'] == 'below'):     #Check if the price falls below the set price
            logger.info("BELOW ALERT TRIGGERED:" + 
                "\n  User: " + userData['first_name'] + 
                "\n  Pair: " + userData['pair'] +
                "\n  Price: " + str(userData['price']) +
                "\n  Current Price: " + str(currentPrice))
            context.bot.send_message(userData['user_id'], "BELOW ALERT!!!!" + 
                "\n  *Pair:* " + userData['pair'] +
                "\n  *Price:* " + str(userData['price']) +
                "\n  *Current Price:* " + str(currentPrice), parse_mode = ParseMode.MARKDOWN)

    elif currentPrice > float(userData['price']):
        if (userData['direction'] == 'above'):     #Check if the price falls below the set price
            logger.info("ABOVE ALERT TRIGGERED:" + 
                "\n  User: " + userData['first_name'] + 
                "\n  Pair: " + userData['pair'] +
                "\n  Price: " + str(userData['price']) +
                "\n  Current Price: " + str(currentPrice))
            context.bot.send_message(userData['user_id'], "ABOVE ALERT!!!!" + 
                "\n  *Pair:* " + userData['pair'] +
                "\n  *Price:* " + str(userData['price']) +
                "\n  *Current Price:* " + str(currentPrice), parse_mode = ParseMode.MARKDOWN)

def conversationTimeout(update, context):
    user = update.message.from_user
    logger.info("The conversation with %s has timed out.", user.first_name)

    update.message.reply_text("This conversation is taking too long, let's do it later 👋")

    return ConversationHandler.END   
def cancel(update, context):
    user = update.message.from_user
    logger.info("%s has cancelled the conversation.", user.first_name)
    update.message.reply_text("Ok, let's do this later", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

#Error Handler
def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        'An exception was raised while handling an update\n'
        '<pre>update = {}</pre>\n\n'
        '<pre>context.chat_data = {}</pre>\n\n'
        '<pre>context.user_data = {}</pre>\n\n'
        '<pre>{}</pre>'
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(str(context.chat_data)),
        html.escape(str(context.user_data)),
        html.escape(tb)
    )

    # Finally, send the message
    context.bot.send_message(chat_id=owner_id, text=message, parse_mode=ParseMode.HTML)

def main():
    """Start the bot."""
    logger.info("Criptonito Core started")

    #Check if there are arguments
    if len(sys.argv)>1:
        #Print the arguments
        #for arg in sys.argv[1:]:
        #    print(arg)
        if sys.argv[1] == "prod":
            logger.warning("---      Executing in Production Mode       ---")
            telegramToken = config.get("telegram", "token_prod")      
    else:
        logger.warning("---      Executing in Dev Mode       ---")
        telegramToken = config.get("telegram", "token_dev")

    
    logger.info("  - Configuration Path: %s", configurationPath)
    logger.info("  - Log Path: %s", ownLogPath)
    logger.info("  - Telegram Token: %s", telegramToken)
    logger.info("Waiting for conversations")

    #Start Bot
    updater = Updater(telegramToken, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler to AddAlert Command
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('addAlert', alertAdd)],
    #     states={
    #         BEGIN: [MessageHandler(Filters.text, alertAdd)],
    #         PAIR: [MessageHandler(Filters.text, alertPair)],
    #         PRICE: [MessageHandler(Filters.text, alertPrice)],
    #         DIRECTION: [MessageHandler(Filters.regex('^(Above|above|Below|below)$'), alertDirection)],
    #         ConversationHandler.TIMEOUT: [MessageHandler(Filters.all, conversationTimeout)]
    #     },

    #     fallbacks=[CommandHandler('cancel', cancel)],
    #     allow_reentry=True,
    #     conversation_timeout = timeout)

    # # on different commands - answer in Telegram
    # dp.add_handler(conv_handler)
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help_command))
    # dp.add_handler(CommandHandler("support", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, checkForPair))
    
    # error handler
    dp.add_error_handler(error_handler)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == '__main__':
    main()