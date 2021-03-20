import asyncio
from asyncio.tasks import all_tasks
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


		

	async def sorcery (self, killer):
		yield
		if self.murderTarget.gameClass != "Prince" and self.murderTarget is not None:

			self.murderTarget.deathCause = "Burnt to Death by [Sorcery]"
			
			self.murderTarget.killer.append(killer)

			await self.makeDead(self.murderTarget)

		yield

	def turnReset (self):
		self.listPlayers.extend(self.listDeadPlayers)
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
	
	async def murder (self, target):
		playerTarget = next(player for player in self.listPlayers if player.name == target)
		self.murderTarget = playerTarget
		self.murderTarget.killer.append(self.getMurderUser())
		sorcerer = self.getClass("Sorcerer")
		if sorcerer is not None:
			await sorcerer.getPrivateTextChannel().send(f"Will you burn [{self.murderTarget.getName()}] to death by using [Sorcery]?")
		knight = self.getClass("Knight")
		if knight is not None:
			await knight.getPrivateTextChannel().send(f"Do you want to kill [{self.murderTarget.getName()}] by using [Deathblow]?")
	
	async def assassination (self, target):
		yield
		playerTarget = next(player for player in self.listPlayers if player.name == target)
		if playerTarget.gameClass == "King" and self.substitutionUsed == True and self.getClass("Double") is not None and self.getClass("Double").status == "Alive":
			playerTarget = self.getClass("Double")

		playerTarget.killer.append(self.getClass("Revolutionary"))
		await self.makeDead(playerTarget)
		yield

	async def deathblow (self, killer):
		yield
		if self.getClass("Sorcerer") is None and self.murderTarget is not None:

			self.murderTarget.deathCause = "Death by [Deathblow]"
			
			self.murderTarget.killer.append(killer)

			#self.listPlayers.remove(self.murderTarget)
			await self.makeDead(self.murderTarget)
		yield

	def substitution(self):
		self.substitutionUsed = True
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
				return next(players for players in self.listPlayers if players.gameClass == "Double")
			else:
				return next(players for players in self.listPlayers if players.gameClass == "King")
		elif "Double" in classes:
			return next(players for players in self.listPlayers if players.gameClass == "Double")
		elif "Prince" in classes:
			return next(players for players in self.listPlayers if players.gameClass == "Prince")
		else:
			return None

	async def makeSecretMeeting (self) -> None:
		
		listTasks = []

		for i in self.secretMeetings:
			listTasks.append(asyncio.create_task(i.arrange()))
		for j in listTasks:
			await j

	async def strike (self, target) -> None:
		playerTarget = next(player for player in self.listPlayers if player.name == target)
		playerTarget.life -= 1
		if playerTarget.life <= 0:
			await self.makeDead(playerTarget)

	def getClass(self, gameClass) -> Player:
		return next(players for players in self.listPlayers if players.gameClass == gameClass)

	def makeTable (self):
		pass

	async def makeDead(self, dead: Player):
		dead.status = "Dead"
		dead.life = 0
		await dead.getPrivateTextChannel().delete()
		await dead.getPrivateVoiceChannel().delete()
		self.listPlayers.remove(dead)
		self.listDeadPlayers.append(dead)
		

	def winning_conditions(self):
		WCKing = False
		WCPrince = False
		WCDouble = False
		WCKnight = False
		WCRevolutionary = False

		IsKingDead = False
		IsPrinceDead = False
		IsDoubleDead = False
		IsKnightDead = False
		IsRevolutionaryDead = False

		for i in self.getListDeadPlayers():
			if i.getClass() == "King":
				IsKingDead = True
			if i.getClass() == "Prince":
				IsPrinceDead = True
			if i.getClass() == "Double":
				IsDoubleDead = True
			if i.getClass() == "Knight":
				IsKnightDead = True
			if i.getClass() == "Revolutionary":
				IsRevolutionaryDead = True

		if (IsPrinceDead == True and IsRevolutionaryDead == True) or (IsKingDead == True):
			WCKing = True
		if (IsKingDead == True and IsDoubleDead == True and IsRevolutionaryDead == True) or (IsPrinceDead == True):
			WCPrince = True
		if (IsPrinceDead == True and IsRevolutionaryDead == True) or (IsDoubleDead == True):
			WCDouble = True
		if (IsKingDead == True and IsPrinceDead == True) or (IsKnightDead == True):
			WCKnight = True
		if (IsKingDead == True and IsPrinceDead == True and IsDoubleDead == True) or (IsRevolutionaryDead == True):
			WCRevolutionary = True

		if (WCKing == True) and (WCPrince == True) and (WCDouble == True) and (WCKnight == True) and (WCRevolutionary == True):
			print("retornei True")
			return True
		else:
			print("Retornei false")
			return False


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
		await self.other.getID().move_to(self.whoRoom.getPrivateVoiceChannel())
		await asyncio.sleep(self.time)
		self.whoRoom.occupied = False
		await self.other.getID().move_to(self.other.getPrivateVoiceChannel())
		self.other.occupied = False
		
