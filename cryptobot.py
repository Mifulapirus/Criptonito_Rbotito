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

from telegramStuff import *
from krakenStuff import *

def main():
    print "-------------------------------"
    print "|     Criptonito_bot 1.0      |"
    print "-------------------------------"

    kraken = Kraken()
    robotito = TelegramBot(kraken)
#sad u'\U0001F629'
#happy u'\U0001F603'

    try:
        while True:
            #Here we can do other stuff, like periodically check for prices in order to send alerts
            #print("im here")
            for chatId in robotito.profiles.iterkeys():
                for key, value in robotito.profiles[chatId].alerts.iteritems():
                    thisAlert = value

                    current_price, current_volume = kraken.getTiket(thisAlert.assetPair)

                    if current_price > 0 and (current_price > thisAlert.maxTriggerPrice or current_price < thisAlert.minTriggerPrice):
                        if current_price > thisAlert.maxTriggerPrice:
                            emoji = u'\U0001F603'
                        else:
                            emoji = u'\U0001F629'

                        print("Alert!!", thisAlert.assetPair, current_price)
                        robotito.sendMessage(chatId, emoji + " Alert: " + thisAlert.assetPair +
                                                " is at " + str(round(current_price, 4)) + " " + u'\u20ac')
                        thisAlert.SetLastPrice(current_price)
                    print thisAlert.assetPair, current_price, thisAlert.maxTriggerPrice, thisAlert.minTriggerPrice

                    #if(currency_pair > value.lastPrice * (1 + (percentage / 100))
                    #self.monitoring[name].lastPrice = current_price

            time.sleep(20)
    except KeyboardInterrupt:
        print("CriptonitoBot is sad and letting you go... :(")
        print("Give me a sec while I kill the threads")

    robotito.killBot()


if __name__ == '__main__':
    main()
