from .strategy import Strategy
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from .strategy_utils import Price, TradeIdea
from exchanges.exchange import Exchange
from typing import Tuple

class DiscordStrategy(Strategy):

  def __init__(self, channel_id: str, messages_xpath: str, ex: Exchange):
    with open('discord.yaml') as config_file:
      config = yaml.safe_load(config_file)

      self.driver = webdriver.Chrome()
      self.driver.get(channel_id)

      time.sleep(5)

      self.driver.find_element(By.NAME, 'email').send_keys(config['username'])
      self.driver.find_element(By.NAME, 'password').send_keys(config['password'])
      self.driver.find_element(By.XPATH, "//button[contains(., 'Log')]").click()

      self.messages_xpath = messages_xpath

      self.ex = ex

      self.used_ideas = set({})

      time.sleep(10)

  def tick(self, dry_run = False, use_multiplier = False):
    messages = self.driver.find_elements(By.XPATH, self.messages_xpath)
    
    for message in messages:
      trade_idea = self.parse_message(message)
      
      if not trade_idea or str(trade_idea) in self.used_ideas:
        continue

      self.used_ideas.add(str(trade_idea))

      if dry_run:
        continue

      print(trade_idea)

      coin, price = self.get_price(trade_idea.coin)
      if not price:
        continue

      print(f"[INFO] Coin {coin} with price {price}")

      if use_multiplier:
        multiplier = price / trade_idea.price.price
        print(f"[INFO] Multiplier is {multiplier}")

        trade_idea.take_profits = [tp*multiplier for tp in trade_idea.take_profits]
        trade_idea.stop_loss *= multiplier
        
        print(f"[INFO] Price of {trade_idea.coin} is {price}, multiplier is {multiplier}")

      print("[INFO] Placing order")
      self.ex.place_orders(coin,
                          trade_idea.price.price,
                          trade_idea.take_profits,
                          trade_idea.stop_loss,
                          trade_idea.trade_side,
                          compute_leverage=True)
      

  def get_price(self, coin) -> Tuple[str, float]:
    try:
      return coin, self.ex.get_price(coin)
    except:
      print(f"[WARN] Couldn't get price for {coin}")
      if coin in _COINS_MULTIPLIER and (
        coin.startswith(
          str(
            int(_COINS_MULTIPLIER[coin])))):
        coin = coin[len(str(
            int(_COINS_MULTIPLIER[coin]))):]
      else:
        coin = "1000" + coin

      try:
        print(f"[WARN] New coin {coin} worked")
        return coin, self.ex.get_price(coin)
      except:
        print(f"[WARN] Couldn't get price for {coin}, skipping trade")
        return None


_COINS_MULTIPLIER = {
  "PEPE": 1000.0,
  "BONK": 1000.0,
  "BEER": 1000.0,
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

_PROMPT = """
I will give you a discord message (possible with an image) that contains information from an analyst about a trade. I would like you to extract that information.

Always use the highest leverage indicated in the post. If there is no leverage indicated use 20x as a default leverage.

If there is no trade to be taken write None

The output should be as following:
first line: name of the token
second line: RISKY if the trade is risky, NOT RISKY otherwise
third line: the price of the token or the word MARKET
4th line: the stop loss price (or word None)
5th line: comma separated list of take profits (or word None)
6th line: DCA
7th line: True if the trade should be trimmed, False otherwise
8th line: True if the trade should be moved to break even
9th line: the leverage

Don't add any extra text. Don't add commas inside numbers

Message: {message}
"""

class DiscordChatGPTStrategy(DiscordStrategy):
  
  def __init__(self, traders_url: str, ex: Exchange):
    super().__init__(traders_url,
                     "ye5h",
                     ex)
    
  def parse_message(self, message: str) -> TradeIdea:
    pass

class DiscordArStrategy(DiscordStrategy):

  def __init__(self, ex: Exchange, discord_url: str = 'https://discord.com/channels/813255168597819444/820224352528105513'):
    super().__init__(discord_url,
                     "//div[contains(@id,'message-content')]",
                     ex)

  def parse_message(self, message: str) -> TradeIdea:
    lines = message.text.split('\n')
    for i in range(len(lines)):
      lines[i] = ''.join([ch for ch in lines[i].strip() if ch.isalnum() or ch == ' ' or ch == '.'])
    words = message.text.split(' ')
    if words[0] not in ('SHORT', 'LONG'):
      return None

    trade_data = lines[0].split(' ')
    # print(trade_data)
    trade_side = trade_data[0]
    ticker = trade_data[1]
    use_market_price = "MARKET" in lines[0]

    try:
      entry_price = float(lines[1].split(' ')[1])
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
          take_profits.append(float(words[-1]))
        elif words[0].startswith('SL'):
          stop_loss = float(words[-1])
      except ValueError:
        return None

    return TradeIdea(trade_side,
                    ticker,
                    Price(use_market_price=use_market_price, price=entry_price),
                    take_profits,
                    stop_loss)
  

class TestArStrategy(DiscordArStrategy):
  def __init__(self, ex: Exchange):
    super().__init__(ex, 'https://discord.com/channels/1116866310769487904/1264706569245954068')