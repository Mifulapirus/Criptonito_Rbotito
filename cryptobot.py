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

    try:
        while True:
            #Here we can do other stuff, like periodically check for prices in order to send alerts
            #print("im here")
            for key, value in robotito.monitoring.iteritems():
                thisAlert = value

                currency_pair, current_price, current_volume = kraken.getTiket(thisAlert.name)
                if current_price > thisAlert.maxTriggerPrice or current_price < thisAlert.minTriggerPrice:
                    print("Alert!!", thisAlert.name, current_price)
                    robotito.sendMessage(thisAlert.chatId, "Pair: " + currency_pair +
                                            " is at " + str(round(current_price, 4)) + " " + u'\u20ac')
                    thisAlert.SetLastPrice(current_price)
                print thisAlert.name, current_price, thisAlert.maxTriggerPrice, thisAlert.minTriggerPrice

                #if(currency_pair > value.lastPrice * (1 + (percentage / 100))
                #self.monitoring[name].lastPrice = current_price

            time.sleep(10)
    except KeyboardInterrupt:
        print("CriptonitoBot is sad and letting you go... :(")
        print("Give me a sec while I kill the threads")

    robotito.killBot()


if __name__ == '__main__':
    main()
