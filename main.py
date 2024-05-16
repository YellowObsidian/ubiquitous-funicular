from exchanges.bybit import BybitExchange
from strategies.discord_strategies import DiscordArStrategy
import time

def main():
    ex = BybitExchange()
    print("CONNECTED TO THE EXCHANGE")

    ar_strategy = DiscordArStrategy()
    print("STRATEGY SET-UP FINISHED")

    while True:
        ar_strategy.tick()
        time.sleep(10)

if __name__ == '__main__':
    main()