from os import name


class Player:
	def __init__(self, name):# -> None:
		self.name = name
		self.gameClass = None
		self.status = "Alive"
		self.life = 3
		self.strike = True
		self.privateChannel = None
	
	def setClass (self, gameClass):
		self.gameClass = gameClass

	def setPrivateChannel (self, channel):
		self.privateChannel = channel
	

		
