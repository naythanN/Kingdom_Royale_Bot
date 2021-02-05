from player import Player

class KingdomRoyale:
	def __init__(self):# -> None:
		self.listPlayers = []
		self.privateChannels = []
		self.secretMeetings = []
		self.bigRoom = None
		self.avaiableClasses = ["King", "Prince", "Double", "Revolutionary", "Sorcerer", "Knight"]

	def addPlayer (self, name):
		self.listPlayers.append(Player(name))
	
	def setPrivateChannel (self, channel, name):
		for i in self.listPlayers:
			if i.name == name:
				i.setPrivateChannel(channel)
		self.privateChannels.append(channel)

	def setSecretMeetings (self, channel):
		self.secretMeetings.append(channel)

	def setBigRoom (self, channel):
		self.bigRoom = channel
