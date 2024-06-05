from exchanges.exchange import Exchange
from abc import ABC, abstractmethod

class Strategy(ABC):

	@abstractmethod
	def tick(self, dry_run: bool):
		pass