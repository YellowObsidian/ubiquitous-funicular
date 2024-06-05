from exchanges.bybit import BybitExchange
from exchanges.mexc import MexcExchange
from strategies.discord_strategies import DiscordArStrategy
import time
import argparse

def main():
    parser = argparse.ArgumentParser(
                    prog='AutoTrade',
                    description='Auto trade')
    parser.add_argument('--exchange', default='mexc', required=False)
    parser.add_argument('--strategy', default='discord_ar', required=False)
    args = parser.parse_args()

    if args.exchange == 'bybit':
        ex = BybitExchange()
    elif args.exchange == 'mexc':
        ex = MexcExchange()
    print("[INFO] CONNECTED TO THE EXCHANGE")
    print(f"[INFO] Exchange server time {ex.get_server_time()}")

    if args.strategy == 'discord_ar':
        strategy = DiscordArStrategy(ex)
    else:
        raise RuntimeError(f"Unknown strategy {parser.exchange}")
    print("[INFO] STRATEGY SET-UP FINISHED")

    strategy.tick(dry_run = False)
    print("[INFO] Dry run finished")
    while True:
        strategy.tick()
        time.sleep(10)

if __name__ == '__main__':
    main()