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
            time.sleep(2)
    except KeyboardInterrupt:
        print("CriptonitoBot is sad and letting you go... :(")
        print("Give me a sec while I kill the threads")

    robotito.killBot()


if __name__ == '__main__':
    main()
