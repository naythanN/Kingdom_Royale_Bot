from os import name


class Player:
	def __init__(self, name, id):# -> None:
		self.name = name
		self.member = id
		self.gameClass = None
		self.status = "Alive"
		self.life = 3
		self.strike = True
		self.privateTextChannel = None
		self.privateVoiceChannel = None
		self.isPlayer = False
		self.deathCause = ""
	
	def setPlayer (self):
		self.isPlayer = True

	def setClass (self, gameClass):
		self.gameClass = gameClass

	def setPrivateTextChannel (self, channel):
		self.privateTextChannel = channel
		
	def setPrivateVoiceChannel (self, channel):
		self.privateVoiceChannel = channel

	def getPrivateTextChannel (self):
		return self.privateTextChannel

	def getPrivateVoiceChannel (self):
		return self.privateVoiceChannel

	def getName(self):
		return self.name
		
	def getClass(self):
		return self.gameClass

	def getID(self):
		return self.member