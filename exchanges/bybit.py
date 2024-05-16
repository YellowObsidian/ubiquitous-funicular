from .exchange import Exchange
from pybit.unified_trading import HTTP
import yaml
import pandas as pd

class BybitExchange(Exchange):
  def __init__(self, testnet = True):
      with open('api.yaml', 'r') as config_file:
          config = yaml.safe_load(config_file)
          self.session =  HTTP(
              testnet=testnet,
              api_key=config['key'],
              api_secret=config['secret'],
          )

  def get_server_time(self):
    return self.session.get_server_time()['time']
  
  def get_ticks(self, symbol: str, interval: str, start: int):
    kline = self.session.get_kline(
        symbol=symbol,
        interval=interval,
        start=start
    )
    return pd.DataFrame(kline['result']['list'],
        columns = ['start_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'turnover'])
  
  def place_order(price: list, takeProfits: list[float], stopLoss: float):
    pass