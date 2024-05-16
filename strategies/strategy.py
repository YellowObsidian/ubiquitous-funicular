from exchanges.exchange import Exchange
from abc import ABC, abstractmethod

class Strategy(ABC):

	@abstractmethod
	def tick(ex: Exchange):
		pass