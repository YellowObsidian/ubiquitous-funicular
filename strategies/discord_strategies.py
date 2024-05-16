from .strategy import Strategy
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class DiscordStrategy(Strategy):

  def __init__(self, channel_id: str):
    with open('discord.yaml') as config_file:
      config = yaml.safe_load(config_file)

      self.driver = webdriver.Chrome()
      self.driver.get(channel_id)

      self.driver.find_element(By.NAME, 'email').send_keys(config['username'])
      self.driver.find_element(By.NAME, 'password').send_keys(config['password'])
      self.driver.find_element(By.XPATH, "//button[contains(., 'Log')]").click()

      time.sleep(5)


class DiscordArStrategy(DiscordStrategy):

  def __init__(self):
    super().__init__('https://discord.com/channels/1060631469996908654/1130095294554583060')

  def tick(self):
    print("TICK")
    pass