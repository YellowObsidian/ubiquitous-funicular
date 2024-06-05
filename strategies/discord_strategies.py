from .strategy import Strategy
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from .strategy_utils import Price, TradeIdea
from exchanges.exchange import Exchange

class DiscordStrategy(Strategy):

  def __init__(self, channel_id: str, messages_xpath: str, ex: Exchange):
    with open('discord.yaml') as config_file:
      config = yaml.safe_load(config_file)

      self.driver = webdriver.Chrome()
      self.driver.get(channel_id)

      self.driver.find_element(By.NAME, 'email').send_keys(config['username'])
      self.driver.find_element(By.NAME, 'password').send_keys(config['password'])
      self.driver.find_element(By.XPATH, "//button[contains(., 'Log')]").click()

      self.messages_xpath = messages_xpath

      self.ex = ex

      self.used_ideas = set({})

      time.sleep(5)


_COINS_MULTIPLIER = {
  "PEPE": 1000.0,
  "BONK": 1000.0,
  "BEER": 1000.0,
  "FLOKI": 1000.0,
  "TURBO": 1000.0,
  "RATS": 1000.0,
  "LADYS": 10*1000.0,
  "MOG": 1000*1000.0,
  "SATS": 10*1000.0,
  "LUNC": 1000.0,
  "WEN": 10.0*1000.0,
  "COQ": 10.0*1000.0,
  "STARL": 10.0*1000.0,
}

class DiscordArStrategy(DiscordStrategy):

  def __init__(self, ex: Exchange):
    super().__init__('https://discord.com/channels/813255168597819444/820224352528105513',
                     "//div[contains(@id,'message-content')]",
                     ex)

  def tick(self, dry_run = False):
    messages = self.driver.find_elements(By.XPATH, self.messages_xpath)
    
    for message in messages:
      trade_idea = self.parse_message(message)
      
      if not trade_idea:
        continue

      if str(trade_idea) in self.used_ideas:
        continue

      self.used_ideas.add(str(trade_idea))

      if dry_run:
        continue

      print(trade_idea)
      try:
        price = self.ex.get_price(trade_idea.coin)
      except:
        print(f"[WARN] Couldn't get price for {trade_idea.coin}")
        trade_idea.coin = "1000" + trade_idea.coin

        try:
          price = self.ex.get_price(trade_idea.coin)
          print(f"[WARN] New coin {trade_idea.coin} worked")
        except:
          print(f"[WARN] Couldn't get price for {trade_idea.coin}, skipping trade")
          continue

      multiplier = _COINS_MULTIPLIER.get(trade_idea.coin, 1.0)

      trade_idea.take_profits = [tp/multiplier for tp in trade_idea.take_profits]
      trade_idea.stop_loss /= multiplier
      
      print(f"[INFO] Price of {trade_idea.coin} is {price}, multiplier is {multiplier}")
      print("[INFO] Placing order")
      self.ex.place_order(trade_idea.coin,
                          None if trade_idea.price.use_market_price else price,
                          trade_idea.take_profits,
                          trade_idea.stop_loss,
                          trade_idea.trade_side)

  def parse_message(self, message: str) -> TradeIdea:
    lines = message.text.split('\n')
    for i in range(len(lines)):
      lines[i] = lines[i].strip()
    words = message.text.split(' ')
    if words[0] not in ('SHORT', 'LONG'):
      return None

    trade_data = lines[0].split(' ')
    trade_side = trade_data[0]
    ticker = trade_data[1][1:]
    use_market_price = "MARKET" in lines[0]

    try:
      entry_price = float(lines[1].split(' ')[1][1:])
    except ValueError:
      return None

    take_profits = []
    stop_loss = 0.0
    for i in range(2, len(lines)):
      words = lines[i].split(' ')
      if len(words) == 0:
        continue
      
      try:
        if words[0].startswith('TP'):
          take_profits.append(float(words[-1][1:]))
        elif words[0].startswith('SL'):
          stop_loss = float(words[-1][1:])
      except ValueError:
        return None

    return TradeIdea(trade_side,
                    ticker,
                    Price(use_market_price=use_market_price, price=entry_price),
                    take_profits,
                    stop_loss)