import asyncio
from asyncio.tasks import all_tasks
from os import kill
from typing import List
from player import Player
import random
import discord
from cancelSleep import cancelableSleep


class SecretMeeting:
    def __init__(self, chooser, chosen) -> None:

        self.time = KingdomRoyale.secretMeetingTime
        self.whoRoom : Player = chooser
        self.other : Player = chosen
        self.task = None
        self.cond : asyncio.Condition = None
        self.skip : int = 0
    def double (self) -> None:
        self.time = self.time*2

    async def arrange (self) -> None:
        while self.whoRoom.occupied == True or self.other.occupied == True:
            await asyncio.sleep(10)
        self.whoRoom.occupied = True
        self.other.occupied = True
        await self.other.getID().move_to(self.whoRoom.getPrivateVoiceChannel())
        self.cond = asyncio.Condition()
        await cancelableSleep(self.time, self.cond)
        self.whoRoom.skipped = False
        self.skip = 0
        self.other.skipped = False
        self.whoRoom.occupied = False
        await self.other.getID().move_to(self.other.getPrivateVoiceChannel())
        self.other.occupied = False

    async def makeTable (self, bigRoom) -> None:
        while self.whoRoom.occupied == True or self.other.occupied == True:
            await asyncio.sleep(1)
        self.whoRoom.occupied = True
        self.other.occupied = True
        await bigRoom.send(f"[{self.whoRoom.name}]       ->     [{self.other.name}]")
        await asyncio.sleep(1)
        self.whoRoom.occupied = False
    
        self.other.occupied = False

        

class KingdomRoyale:
    secretMeetingTime : int = 90
    cond : asyncio.Condition = asyncio.Condition()

    def __init__(self):# -> None:
        self.listPlayers : List[Player] = []
        self.listDeadPlayers : List[Player] = []
        self.privateTextChannels = []
        self.privateVoiceChannels = []
        self.pastPlayers = []
        self.bigRoomV = None
        self.graveyard = None
        self.taskTimeTable = None
        self.taskTurn = None
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
        self.secretMeetingTime : int = 90
        self.sleepBigRoom : int = 180
        self.sleepTimeTable : int = 30
        self.currentBlock : str = ""
        self.mode = "Pairs"
        self.bigRoomSkip = 0
        self.gameStarted = False
        self.guild = None
        self.currentDay = "First"
        self.victoryConditions = {
            "King"          : ["Prince","Revolutionary"],
            "Prince"        : ["King", "Double", "Revolutionary"],
            "Double"        : ["Prince", "Revolutionary"],
            "Sorcerer"      : [],
            "Knight"        : ["King", "Prince"],
            "Revolutionary" : ["King", "Prince", "Double"]
        }

        

    async def sorcery (self, killer : Player):
        yield
        if self.murderTarget.gameClass != "Prince" and self.murderTarget is not None:

            self.murderTarget.deathCause = f"Killed on the {self.currentDay} day by {self.getMurderUser().name} and {killer.name}'s [Sorcery]"
            killer.listKilled.append(f"Killed {self.murderTarget.name} using [Sorcery] on the {self.currentDay} day. ")
            self.getMurderUser().listKilled.append(f"Killed {self.murderTarget.name} on the {self.currentDay} day by selecting him as the target of [Murder]. ")
            self.murderTarget.killer.append(killer)
            await self.getBigRoomChat().send(f"[{self.murderTarget.name}], burnt to death by [Sorcery]")
            await self.makeDead(self.murderTarget)

        yield

    async def turnReset (self):
        for i in self.listDeadPlayers:
            i.life = 5
            i.status = "Alive"
            i.deathCause = ""

        for i in self.listPlayers:
            await i.getPrivateTextChannel().delete()
            await i.getID().move_to(self.graveyard)
            await i.getPrivateVoiceChannel().delete()
        
        self.listPlayers.extend(self.listDeadPlayers)
        self.listDeadPlayers = []
        
        for i in self.getListPlayers():
            overwrites = {
                self.guild.default_role : discord.PermissionOverwrite(read_messages=False),
                self.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            await self.setPrivateTextChannel(await self.guild.create_text_channel(i.name + "'s room", overwrites = overwrites), i.name)

            await self.setPrivateVoiceChannel(await self.guild.create_voice_channel(i.name + "'s room", overwrites = overwrites), i.name)
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
        #self.murderTarget.killer.append(self.getMurderUser())
        sorcerer = self.getClass("Sorcerer")
        if sorcerer is not None:
            await sorcerer.getPrivateTextChannel().send(f"Will you burn [{self.murderTarget.getName()}] to death by using [Sorcery]?")
        knight = self.getClass("Knight")
        
        if knight is not None and sorcerer is None:
            await knight.getPrivateTextChannel().send(f"Do you want to kill [{self.murderTarget.getName()}] by using [Deathblow]?")
    
    async def assassination (self, target):
        yield
        playerTarget = next(player for player in self.listPlayers if player.name == target)
        if playerTarget.gameClass == "King" and self.substitutionUsed == True and self.getClass("Double") is not None and self.getClass("Double").status == "Alive":
            playerTarget = self.getClass("Double")
        playerTarget.deathCause = f"Killed on the {self.currentDay} day by {self.getClass('Revolutionary').name}'s [Assassination]. "
        playerTarget.killer.append(self.getClass("Revolutionary"))
        self.getClass("Revolutionary").listKilled.append(f"Killed {target} using [Assassination] on the {self.currentDay} day. ")
        await self.makeDead(playerTarget)
        await self.getBigRoomChat().send(f"[{target}] was strangulated by [Assassination]")
        yield

    async def deathblow (self, killer : Player):
        yield
        if self.getClass("Sorcerer") is None and self.murderTarget is not None and self.murderTarget in self.listPlayers:

            killer.listKilled.append(f"Killed {self.murderTarget.name} using [Deathblow] on the {self.currentDay} day. ")
            self.getMurderUser().listKilled.append(f"Killed {self.murderTarget.name} on the {self.currentDay} day by selecting him as the target of [Murder]. ")
            self.murderTarget.deathCause = f"Killed on the {self.currentDay} day by {self.getMurderUser().name} and {killer.name}'s [Deathblow]. "
            
            self.murderTarget.killer.append(killer)
            await self.getBigRoomChat().send(f"[{self.murderTarget.name}], death by [Deathblow]")
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

    def getPlayer (self, name: str):
        for i in self.listPlayers:
            if i.name == name:
                return i
        return None

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
        
        listMeetings = []
        await self.getBigRoomChat().send("Secret Meetings")

        for i in self.secretMeetings:
            listMeetings.append(asyncio.create_task(i.makeTable(self.getBigRoomChat())))
        for j in listMeetings:
            await j

        for i in self.secretMeetings:
            i.task = asyncio.create_task(i.arrange())
        for j in self.secretMeetings:
            await j.task

    async def strike (self, striker : Player, target) -> None:
        playerTarget = next(player for player in self.listPlayers if player.name == target)
        playerTarget.life -= 1
        if self.currentBlock == "B" or self.currentBlock == "D":
            await self.getBigRoomChat().send(f"[{target}] has been striked by {striker.name}.")
        if playerTarget.life <= 0:
            playerTarget.deathCause = f"Killed directly on the {self.currentDay} day by {striker.name}."
            
            striker.listKilled.append(f"Killed {target} directly on the {self.currentDay} day.")
            await self.getBigRoomChat().send(f"[{target}] has bleed to death")
            await self.makeDead(playerTarget)

    def canStrike(self, striker: Player, striked: Player) -> bool:
        if striked is not None and striker.strike == True and striked.status == "Alive" and (striker.pair != striked or striker.isPlayer == True):
            if self.currentBlock == "B" or self.currentBlock == "D":
                return True
            elif self.currentBlock == "C":
                for i in self.secretMeetings:
                    if striker in [i.whoRoom, i.other] and striked in [i.whoRoom, i.other]:
                        return True
        return False

    def getClass(self, gameClass) -> Player:
        listP = [players for players in self.listPlayers if players.gameClass == gameClass]
        if len(listP) > 0:
            return listP[0]

    def getClassDead(self, gameClass) -> Player:
        listP = [players for players in self.listDeadPlayers if players.gameClass == gameClass]
        if len(listP) > 0:
            return listP[0]
    
    async def makeDead(self, dead: Player):
        dead.status = "Dead"
        dead.life = 0
        await dead.getID().move_to(self.graveyard)
        await dead.getPrivateTextChannel().delete()
        await dead.getPrivateVoiceChannel().delete()
        self.listPlayers.remove(dead)
        self.listDeadPlayers.append(dead)
        if self.winning_conditions():
            self.taskTurn.cancel()
        
    def makePairs (self):
        numberOfPairs = 0
        for i in self.listPlayers:
            if i.pair is None and numberOfPairs < 2:
                possiblePair = [j for j in self.listPlayers if j.pair is None and j != i]
                if possiblePair.__len__() > 0:
                    numberPlayer = int(random.uniform(0, len(possiblePair)))
                    possiblePair[numberPlayer].pair = i
                    i.pair = possiblePair[numberPlayer]
                    numberOfPairs += 1

    async def display (self):
        bigRoom = self.getBigRoomChat()
        await bigRoom.send ("\n********** GAME OVER ***********")
        await bigRoom.send("\nWinners")
        string = ""
        for i in self.listPlayers:
            if i.diedAsPlayer == False:
                i.score += 1
            string += f'\n[{i.name}] {"(Player)" if i.isPlayer else ""}\n'
            string += f'[{i.gameClass}] score = {i.score}\n'
            for j in i.listKilled:
                string += j
            string += " Alive.\n"
            string += "* Victory conditions have been met due to "
            for j in self.victoryConditions[i.gameClass]:
                if self.getClassDead(j).gameClass == "Sorcerer":
                    string += " them surving."
                else:
                    string += f"{self.getClassDead(j).name} ,"
            string += ("'s death.\n")
            
        string +=  ("\nLoosers")
        for i in self.listDeadPlayers:
            if i.isPlayer:
                i.score = 0
                i.diedAsPlayer = True
            string += f'\n[{i.name}] {"(Player)" if i.isPlayer else ""}\n'
            string += f'[{i.gameClass}] score = {i.score}\n'
            for j in i.listKilled:
                string +=  (j)
            string += i.deathCause
        await bigRoom.send(string)
        await asyncio.sleep(30)

    async def winning_conditions(self):
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
            await self.display()
            return True
        else:
            print("Retornei false")
            return False

