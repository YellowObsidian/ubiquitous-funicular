from .exchange import Exchange
from pybit.unified_trading import HTTP
import yaml
from typing import Optional

class BybitExchange(Exchange):
  def __init__(self, testnet = True):
      super().__init__()
      with open(self.config_file, 'r') as config_file:
          config = yaml.safe_load(config_file)
          self.session =  HTTP(
              testnet=testnet,
              api_key=config['key'],
              api_secret=config['secret'],
          )

  def get_server_time(self):
    return int(self.session.get_server_time()['time'])
  
  def get_price(self, coin: str):
    price_data = self.session.get_tickers(
        category = 'linear',
        symbol = self.get_symbol(coin),
     )
    print(price_data)
    return float(price_data['result']['list'][0]['lastPrice'])
  
  def submit_order(self,
       symbol: str,
       direction: str,
       price: float,
       vol: float,
       side: str,
       type: str,
       stopLossPrice: Optional[float] = None,
       leverage: Optional[int] = None,
       openType: str = "CROSS"):
    
    if direction == "OPEN" and side == "LONG":
       sideI = "Buy"
    if direction == "CLOSE" and side == "SHORT":
       sideI = "Buy"
    if direction == "OPEN" and side == "SHORT":
       sideI = "Sell"
    if direction == "CLOSE" and side == "LONG":
       sideI = "Sell"

    kwargs = {
       'category': "linear",
       'symbol': symbol,
       'side': sideI,
       'orderType': type.lower().capitalize(),
       'price': ("%.2f" % price),
       'qty': int(vol),
       'side': sideI,
    }

    if stopLossPrice:
       kwargs['stopLoss'] = "%.2f" % stopLossPrice

    try:
      self.session.set_leverage(
        category = 'linear',
        symbol = symbol, 
        buyLeverage = '10',
        sellLeverage = '10')
    except:
       pass
    return self.session.place_order(**kwargs)

  def get_symbol(self, coin: str) -> str:
     return coin + "USDT"