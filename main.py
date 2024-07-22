from exchanges.bybit import BybitExchange
from exchanges.mexc import MexcExchange
from strategies.discord_strategies import DiscordArStrategy, TestArStrategy
import time
import argparse

def main():
    parser = argparse.ArgumentParser(
                    prog='AutoTrade',
                    description='Auto trade')
    parser.add_argument('--exchange', default='bybit', required=False)
    parser.add_argument('--strategy', default='discord_ar_test', required=False)
    args = parser.parse_args()

    if args.exchange == 'bybit':
        ex = BybitExchange(testnet=True)
    elif args.exchange == 'mexc':
        ex = MexcExchange()

    print("[INFO] CONNECTED TO THE EXCHANGE")
    print(f"[INFO] Exchange server time {ex.get_server_time()}")

    if args.strategy == 'discord_ar':
        strategy = DiscordArStrategy(ex)
    elif args.strategy == 'discord_ar_test':
        strategy = TestArStrategy(ex)
    else:
        raise RuntimeError(f"Unknown strategy {parser.exchange}")
    print("[INFO] STRATEGY SET-UP FINISHED")

    time.sleep(5)

    strategy.tick(dry_run = True)
    print("[INFO] Dry run finished")
    while True:
        strategy.tick()
        time.sleep(10)

if __name__ == '__main__':
    main()