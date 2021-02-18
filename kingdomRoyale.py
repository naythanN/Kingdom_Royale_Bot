from os import kill
from typing import List
from player import Player
import random
import discord


class KingdomRoyale:
	def __init__(self):# -> None:
		self.listPlayers = []
		self.listDeadPlayers = []
		self.privateTextChannels = []
		self.privateVoiceChannels = []
		self.pastPlayers = []
		self.bigRoomV = None
		self.taskTimeTable = None
		self.bigRoomC = None
		self.avaiableClasses = ["King", "Prince", "Double", "Revolutionary", "Sorcerer", "Knight"]
		self.classToPick = ["King", "Prince", "Double", "Revolutionary", "Sorcerer", "Knight"]
		self.days = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh"]
		self.player = None
		self.murderTarget : Player = None
		self.substitutionUsed = False
		self.canUseSubstitution = True

		

	def sorcery (self, killer):
		self.murderTarget.life = 0
		self.murderTarget.status = "Dead"
		self.murderTarget.deathCause = "Burnt to Death by [Sorcery]"
		
		self.murderTarget.killer.append(killer)

		self.listPlayers.remove(self.murderTarget)

	def turnReset (self):
		pass
	
	def murder (self, target, killer):
		playerTarget = next(player for player in self.listPlayers if player.name == target)
		self.murderTarget = playerTarget
		self.murderTarget.killer.append(self.getMurderUser())

	
	def assassination (self):
		pass

	def deathblow (self, killer):
		pass

	def substitution(self):
		self.substituionUsed = True

	def addPlayer (self, id):
		self.listPlayers.append(Player(id.name, id))
	
	def setPlayer (self):
		possiblePlayers = [i for i in self.listPlayers if i not in self.pastPlayers]

		numberPlayer = int(random.uniform(0, len(possiblePlayers)))
		possiblePlayers[numberPlayer].setPlayer()
		self.player = possiblePlayers[numberPlayer]

	def setClasses (self):
		for i in self.listPlayers:
			numberClass = int(random.uniform(0, len(self.classToPick)))
			i.setClass(self.classToPick[numberClass])
			self.classToPick.remove(self.classToPick[numberClass])
		

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

	def getListPlayers(self) -> List[Player]:
		return self.listPlayers

	def getDays(self):
		return self.days

	def getBigRoomChat(self) -> discord.guild.TextChannel:
		return self.bigRoomC

	def getBigRoomVoice(self) -> discord.guild.VoiceChannel:
		return self.bigRoomV
	
	def getPrivateTextChannel(self, name) -> discord.guild.TextChannel:
		for i in self.listPlayers:
			if i.name == name:
				return i.getPrivateTextChannel()

	def getPrivateVoiceChannel(self, name) -> discord.guild.VoiceChannel:
		for i in self.listPlayers:
			if i.name == name:
				return i.getPrivateVoiceChannel()

	def getAllPrivateTextChannels(self) -> List[discord.guild.TextChannel]:
		return self.privateTextChannels

	def getAllPrivateVoiceChannels(self) -> List[discord.guild.VoiceChannel]:
		return self.privateVoiceChannels

	def getMurderUser (self) -> Player:
		classes = [classes.gameClass for classes in self.listPlayers]
		if "King" in classes:
			if self.substitutionUsed == True:
				return next([players for players in self.listPlayers if players.gameClass == "Double"])
			else:
				return next([players for players in self.listPlayers if players.gameClass == "King"])
		elif "Double" in classes:
			return next([players for players in self.listPlayers if players.gameClass == "Double"])
		elif "Prince" in classes:
			return next([players for players in self.listPlayers if players.gameClass == "Prince"])
		else:
			return None

	