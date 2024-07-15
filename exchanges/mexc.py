from .exchange import Exchange
from pymexc import futures
import yaml
from typing import Optional

class MexcExchange(Exchange):
  def __init__(self):
      super().__init__()
      with open(self.config_file, 'r') as config_file:
          config = yaml.safe_load(config_file)
          self.http_session =  futures.HTTP(
              api_key=config['key'],
              api_secret=config['secret'],
          )
          self.websocket_session = futures.WebSocket(
              api_key=config['key'],
              api_secret=config['secret'],
          )

  def get_server_time(self) -> int:
    return self.http_session.ping()['data']
   
  def get_price(self, coin: str) -> float:
      x = self.http_session.kline(self.get_symbol(coin), "Min1")["data"]
      return x["close"][-1]
       
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
       sideI = 1
    if direction == "CLOSE" and side == "SHORT":
       sideI = 2
    if direction == "OPEN" and side == "SHORT":
       sideI = 3
    if direction == "CLOSE" and side == "LONG":
       sideI = 4

    kwargs = {
       'symbol': symbol,
       'price': price,
       'vol': vol,
       'side': sideI,
       'type': 1 if type == "LIMIT" else 5,
       'stop_loss_price': stopLossPrice,
       'leverage': leverage,
       'open_type': 1 if openType == "ISOLATED" else 2
    }

    return self.http_session.order(**kwargs)

  def get_symbol(self, coin: str) -> str:
     return coin + "_USDT"