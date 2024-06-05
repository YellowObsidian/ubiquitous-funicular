from .exchange import Exchange
from pymexc import futures
import yaml

class MexcExchange(Exchange):
  def __init__(self):
      with open('mexc_api.yaml', 'r') as config_file:
          config = yaml.safe_load(config_file)
          self.http_session =  futures.HTTP(
              api_key=config['key'],
              api_secret=config['secret'],
          )
          self.websocket_session = futures.WebSocket(
              api_key=config['key'],
              api_secret=config['secret'],
          )
      
      with open('config.yaml', 'r') as config_file:
         config = yaml.safe_load(config_file)
         self.contract_price = config['contract_price']

  def get_server_time(self) -> int:
    return self.http_session.ping()['data']
   
  def get_price(self, coin: str) -> float:
      x = self.http_session.kline(self.get_symbol(coin), "Min1")["data"]
      return x["close"][-1]
  
  def place_order(self,
                coin: str,
                price: float,
                takeProfits: list[float],
                stopLoss: float,
                side: str) -> None:
    symbol = self.get_symbol(coin)
    price = price if price else self.get_price(coin)
    vol = self.contract_price / price
    print(f"[INFO] Vol {vol}, price {price}, stop loss {stopLoss}")

    # submit main trade
    res = self.http_session.order(
       symbol = symbol,
       price = price,
       vol = vol,
       side = 1 if side == "LONG" else 3,
       type = 5, # market order
       stop_loss_price = stopLoss,
       leverage = 10,
       open_type = 2, # cross
    )
    print(res)

    for takeProfit in takeProfits:
      print(f"[INFO] Adding take profit {takeProfit}")
      self.http_session.order(
        symbol = symbol,
        price = takeProfit,
        vol = vol*0.4,
        side = 4 if side == "LONG" else 2,
        type = 1, # limit order
        open_type = 2, # cross
      )
      print(res)
       

  def get_symbol(self, coin: str) -> str:
     return coin + "_USDT"