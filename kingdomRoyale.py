import asyncio
from os import kill
from typing import List
from player import Player
import random
import discord



class KingdomRoyale:
	secretMeetingTime : int = 20

	def __init__(self):# -> None:
		self.listPlayers : List[Player] = []
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
		self.actions = []
		self.secretMeetings : List[SecretMeeting] = []
		self.secretMeetingTime : int = 20
		self.sleepTimeTable : int = 30


		

	def sorcery (self, killer):
		yield
		if self.murderTarget.gameClass != "Prince":

			self.murderTarget.life = 0
			self.murderTarget.status = "Dead"
			self.murderTarget.deathCause = "Burnt to Death by [Sorcery]"
			
			self.murderTarget.killer.append(killer)

			self.listPlayers.remove(self.murderTarget)

		yield

	def turnReset (self):
		self.listDeadPlayers = []
		self.avaiableClasses = ["King", "Prince", "Double", "Revolutionary", "Sorcerer", "Knight"]
		self.classToPick = ["King", "Prince", "Double", "Revolutionary", "Sorcerer", "Knight"]
		self.player = None
		self.murderTarget : Player = None
		self.substitutionUsed = False
		self.canUseSubstitution = True
		self.actions = []
		self.secretMeetings : List[SecretMeeting] = []
		self.secretMeetingTime : int = 10
	
	def murder (self, target):
		playerTarget = next(player for player in self.listPlayers if player.name == target)
		self.murderTarget = playerTarget
		self.murderTarget.killer.append(self.getMurderUser())

	
	def assassination (self, target):
		yield
		playerTarget = next(player for player in self.listPlayers if player.name == target)
		if playerTarget.gameClass == "King" and self.substituionUsed == True:
			self.murderTarget = self.getClass("Double")
		else:
			self.murderTarget = playerTarget
		self.murderTarget.killer.append(self.getClass("Revolutionary"))
		yield

	def deathblow (self, killer):
		yield
		self.murderTarget.life = 0
		self.murderTarget.status = "Dead"
		self.murderTarget.deathCause = "Death by [Deathblow]"
		
		self.murderTarget.killer.append(killer)

		self.listPlayers.remove(self.murderTarget)
		yield

	def substitution(self):
		self.substituionUsed = True
		self.canUseSubstitution = False

	def addPlayer (self, id):
		self.listPlayers.append(Player(id.name, id))
	
	def setPlayer (self):
		possiblePlayers = [i for i in self.listPlayers if i not in self.pastPlayers]

		numberPlayer = int(random.uniform(0, len(possiblePlayers)))
		possiblePlayers[numberPlayer].setPlayer()
		self.player = possiblePlayers[numberPlayer]

	def setClasses (self):
		for i in self.listPlayers:
			if i.isPlayer == False:
				numberClass = int(random.uniform(0, len(self.classToPick)))
				i.setClass(self.classToPick[numberClass])
				self.classToPick.remove(self.classToPick[numberClass])
		

	async def setPrivateTextChannel (self, channel, name):
		for i in self.listPlayers:
			if i.name == name:
				await channel.set_permissions(i.getID(), read_messages = True)
				i.setPrivateTextChannel(channel)
		self.privateTextChannels.append(channel)

	async def setPrivateVoiceChannel (self, channel, name):
		for i in self.listPlayers:
			if i.name == name:
				await channel.set_permissions(i.getID(), read_messages = True)
				i.setPrivateVoiceChannel(channel)
		self.privateVoiceChannels.append(channel)

	def setBigRoomV (self, channel):
		self.bigRoomV = channel

	def setBigRoomC (self, channel):
		self.bigRoomC = channel

	def getListPlayers(self) -> List[Player]:
		return self.listPlayers

	def getListDeadPlayers(self):
		return self.listDeadPlayers

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

	def makeSecretMeeting (self) -> None:
		for i in self.secretMeetings:
			asyncio.create_task(i.arrange())

	def getClass(self, gameClass) -> Player:
		return next([players for players in self.listPlayers if players.gameClass == gameClass])

	def makeTable (self):
		pass


class SecretMeeting:
	def __init__(self, chooser, chosen) -> None:

		self.time = KingdomRoyale.secretMeetingTime
		self.whoRoom : Player = chooser
		self.other : Player = chosen
	
	def double (self) -> None:
		self.time = self.time*2

	async def arrange (self) -> None:
		while self.whoRoom.occupied == True or self.other.occupied == True:
			await asyncio.sleep(KingdomRoyale.secretMeetingTime)
		self.whoRoom.occupied = True
		self.other.occupied = True
		self.other.getID().move_to(self.whoRoom.getPrivateVoiceChannel())
		await asyncio.sleep(self.time)
		self.whoRoom.occupied = False
		self.other.getID().move_to(self.other.getPrivateVoiceChannel())
		self.other.occupied = False
		
