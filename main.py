from pybit.unified_trading import HTTP
import plotly.graph_objects as go
import pandas as pd
from strategies.strategy import Strategy
import yaml

def connect(testnet=True):
    with open('api.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        return HTTP(
            testnet=testnet,
            api_key=config['key'],
            api_secret=config['secret'],
        )

def get_milis(days = 0, hours = 0, minutes = 0):
    minutes = minutes + 60*hours + 24*60*days
    return minutes * 60 * 1000

def get_kline_df(symbol, interval, start):
    kline = session.get_kline(
        symbol=symbol,
        interval=interval,
        start=start
    )
    return pd.DataFrame(kline['result']['list'],
        columns = ['start_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'turnover'])

def get_candlestick_fig(price_df):
    return go.Figure(data=[go.Candlestick(x=list(reversed(price_df['start_time'])),
                open=list(reversed(price_df['open_price'])),
                high=list(reversed(price_df['high_price'])),
                low=list(reversed(price_df['low_price'])),
                close=list(reversed(price_df['close_price'])))])

def get_server_time():
    return session.get_server_time()['time']

session = connect()

price_df = get_kline_df('BTCUSDT', 'D', get_server_time() - get_milis(days=30))
fig = get_candlestick_fig(price_df)
fig.show()