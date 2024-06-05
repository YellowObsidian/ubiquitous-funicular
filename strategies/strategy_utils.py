class Price:
    def __init__(self, use_market_price : bool = False, price : float = 0.0):
      self.price = price
      self.use_market_price = use_market_price

class TradeIdea:
  def __init__(self,
               trade_side : str,
               coin : str,
               price : Price,
               take_profits : list[float],
               stop_loss = float):
    self.trade_side = trade_side
    self.coin = coin
    self.price = price
    self.take_profits = take_profits
    self.stop_loss = stop_loss

  def __str__(self):
     return f"{self.trade_side} {self.coin} {self.price.use_market_price} {self.price.price} {self.take_profits} {self.stop_loss}"