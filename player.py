from os import name

import discord
from typing import List

class Player:
    def __init__(self, name, id):# -> None:
        self.name = name
        self.member = id
        self.gameClass = None
        self.status = "Alive"
        self.life = 5
        self.strike = True
        self.privateTextChannel = None
        self.privateVoiceChannel = None
        self.isPlayer = False
        self.killer = []
        self.deathCause = ""
        self.listKilled : List[str] = []
        self.score = 0
        self.diedAsPlayer : bool = False
        self.occupied = False
        self.skipped = False
        self.pair : Player = None
        
    
    def setPlayer (self):
        self.isPlayer = True

    def setClass (self, gameClass):
        self.gameClass = gameClass

    def setPrivateTextChannel (self, channel):
        self.privateTextChannel = channel
        
    def setPrivateVoiceChannel (self, channel):
        self.privateVoiceChannel = channel

    def getPrivateTextChannel (self) -> discord.guild.TextChannel:
        return self.privateTextChannel

    def getPrivateVoiceChannel (self) -> discord.guild.VoiceChannel:
        return self.privateVoiceChannel

    def getName(self):
        return self.name
        
    def getClass(self):
        return self.gameClass

    def getID(self) -> discord.Member:
        return self.member

