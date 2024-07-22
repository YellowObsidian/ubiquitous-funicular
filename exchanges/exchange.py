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
                side: str,
                vol_multiplier: float = 0.25,
                compute_leverage: bool = False) -> None:
    symbol = self.get_symbol(coin)
    price = price if price else self.get_price(coin)
    print(f"PLACING ORDER WITH PRICE {price}")

    if compute_leverage:
      vol = self.contract_price / abs(price - stopLoss)
      leverage = "%.2f" % ((vol * price) / self.contract_price)
    else:
      vol = self.contract_price / price
      leverage = self.leverage

    print(f"[INFO] Vol {vol}, price {price}, stop loss {stopLoss}, leverage {leverage}")

    # submit main trade
    res = self.submit_order(
       symbol = symbol,
       direction = "OPEN",
       price = price,
       vol = vol,
       side = side,
       type = "LIMIT",
       stopLossPrice = stopLoss,
       leverage = leverage,
       openType = "CROSS",
    )
    print(res)

    for takeProfit in takeProfits:
      print(f"[INFO] Adding take profit {takeProfit}, vol {vol*vol_multiplier}")
      if vol*vol_multiplier <= 0.01:
        break
      
      try:
        # self.submit_order(
        #   symbol = symbol,
        #   direction = "CLOSE",
        #   price = takeProfit,
        #   vol = vol*vol_multiplier,
        #   side = side,
        #   type = "LIMIT",
        #   openType = "CROSS",
        # )
        # res = self.session.set_trading_stop(
        #   category = "linear",
        #   symbol = symbol,
        #   takeProfit = takeProfit,
        #   stopLoss = stopLoss,
        #   tpSize = str(vol*vol_multiplier),
        #   slSize = str(vol*vol_multiplier),
        #   tpslMode = "Partial",
        #   positionIdx = 0,
        # )
        vol *= vol_multiplier
      except Exception as e:
        print(res)
        print(f"[WARN] Couldn't make the trade: {e}")