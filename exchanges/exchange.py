import yaml

class Exchange:
  def __init__(self):
    with open('config.yaml', 'r') as config_file:
         config = yaml.safe_load(config_file)
         self.contract_price = config['contract_price']
         self.leverage = config['leverage']
         self.config_file = f"{config['exchange_api_file']}.yaml"

  def get_server_time(self) -> int:
    pass

  def get_ticks(self, symbol: str, interval: str, start: int):
    pass

  def get_wallet():
    pass

  def get_price(coin: str):
    pass

  def get_symbol(coin: str):
    pass

  def place_orders(self,
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
    res = self.submit_order(
       symbol = symbol,
       direction = "OPEN",
       price = price,
       vol = vol,
       side = side,
       type = "MARKET",
       stopLossPrice = stopLoss,
       leverage = self.leverage,
       openType = "CROSS",
    )
    print(res)

    for takeProfit in takeProfits:
      print(f"[INFO] Adding take profit {takeProfit}, vol {vol*0.4}")
      if vol*0.4 <= 0.01:
        break
      
      try:
        self.submit_order(
          symbol = symbol,
          direction = "CLOSE",
          price = takeProfit,
          vol = vol*0.4,
          side = side,
          type = "LIMIT",
          openType = "CROSS",
        )
        vol *= 0.40
        print(res)
      except:
        print("[WARN] Couldn't make the trade")