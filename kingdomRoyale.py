from player import Player

class KingdomRoyale:
	def __init__(self):# -> None:
		self.listPlayers = []
		self.listDeadPlayers = []
		self.privateTextChannels = []
		self.privateVoiceChannels = []
		self.bigRoomV = None
		self.taskTimeTable = None
		self.bigRoomC = None
		self.avaiableClasses = ["King", "Prince", "Double", "Revolutionary", "Sorcerer", "Knight"]
		self.days = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh"]

	def addPlayer (self, id):
		self.listPlayers.append(Player(id.name, id))
	
	def setPrivateTextChannel (self, channel, name):
		for i in self.listPlayers:
			if i.name == name:
				i.setPrivateTextChannel(channel)
		self.privateTextChannels.append(channel)

	def setPrivateVoiceChannel (self, channel, name):
		for i in self.listPlayers:
			if i.name == name:
				i.setPrivateVoiceChannel(channel)
		self.privateVoiceChannels.append(channel)

	def setBigRoomV (self, channel):
		self.bigRoomV = channel

	def setBigRoomC (self, channel):
		self.bigRoomC = channel

	def getListPlayers(self):
		return self.listPlayers

	def getDays(self):
		return self.days

	def getBigRoomChat(self):
		return self.bigRoomC

	def getBigRoomVoice(self):
		return self.bigRoomV
	
	def getPrivateTextChannel(self, name):
		for i in self.listPlayers:
			if i.name == name:
				return i.getPrivateTextChannel()

	def getPrivateVoiceChannel(self, name):
		for i in self.listPlayers:
			if i.name == name:
				return i.getPrivateVoiceChannel()

	def getAllPrivateTextChannels(self):
		return self.privateTextChannels

	def getAllPrivateVoiceChannels(self):
		return self.privateVoiceChannels
