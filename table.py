
from player import Player
from kingdomRoyale import KingdomRoyale, SecretMeeting
import asyncio
from cancelSleep import cancelableSleep
import jsonpickle
import json

import logging
from logConfig import myLogger, jsonLogger


async def turnLoop (ctx, game : KingdomRoyale):
    logger = myLogger()
    i = 0
    if game.mode == "Pairs":
        game.makePairs()
    while i < 7:
        game.secretMeetings.clear()
        bigRoomC = game.getBigRoomChat()
        bigRoomV = game.getBigRoomVoice()
        game.currentBlock = "A"
        serial = jsonpickle.encode(game)
        jsonLogger(serial)
        game.currentDay = game.getDays()[i]
        await bigRoomC.send(f"{game.getDays()[i]} Day <A> owns's room")

        for j in game.getListPlayers():
            j.life += 1
            if j.life > len(game.getListPlayers()) - 1:
                j.life = len(game.getListPlayers()) - 1
            j.strike = True
            personRoom = game.getPrivateTextChannel(j.name)
            await personRoom.send(f"{game.getDays()[i]} Day <A> [{j.name}]'s room")
            if i == 0 and j.pair is not None:
                await personRoom.send(f"Your dear friend {j.pair.name} is also in the game, you wouldn't want anything bad to happen to him right?")
            if j.isPlayer == True and i == 0:
                await personRoom.send(f"Gufufu - PleaSed to - meEt you - {j.name}-kun - Alright - you wiLl now - select yOur [class]")
            await j.getID().move_to(j.getPrivateVoiceChannel())
        if i == 0:
            await cancelableSleep(1000, game.cond, game)
        await asyncio.sleep(10)
        await game.bigRoomC.set_permissions(game.guild.default_role, read_messages=True)
        game.currentBlock = "B"
        serial = jsonpickle.encode(game)
        jsonLogger(serial)
        if i == 0:
            game.setClasses()
        await bigRoomC.send(f"{game.getDays()[i]} Day <B> Big room")
        for j in game.getListPlayers():
            await j.getID().move_to(bigRoomV)

        await cancelableSleep(game.sleepBigRoom, game.cond, game)
        game.bigRoomSkip = 0
        game.currentBlock = "C"
        serial = jsonpickle.encode(game)
        jsonLogger(serial)
        
        await bigRoomC.send(f"{game.getDays()[i]} Day <C> owns's room")
        if i == 0:
            
            for j in game.getListPlayers():
                personRoom = game.getPrivateTextChannel(j.name)
                await personRoom.send(f"Your [class] is [{j.gameClass}]")

        for j in game.getListPlayers():
            j.skipped = False
            personRoom = game.getPrivateTextChannel(j.name)
            await j.getID().move_to(j.getPrivateVoiceChannel())
            if j.getClass() == "Sorcerer":
                if game.murderTarget is None:
                    await personRoom.send(f"No target has been selected for [Murder] yet.")
                else:
                    await personRoom.send(f"Will you burn [{game.murderTarget.getName()}] to death by using [Sorcery]?")
            if j.getClass() == "Knight":
                classes = [classes.gameClass for classes in game.getListPlayers()]
                if game.murderTarget is None and "Sorcerer" not in classes:
                    await personRoom.send(f"No target has been selected for [Murder] yet.")
                elif game.murderTarget is not None and "Sorcerer" not in classes:
                    await personRoom.send(f"Do you want to kill [{game.murderTarget.getName()}] by using [Deathblow]?")
            if j.getClass() == "King":
                if j == game.getMurderUser():
                    await personRoom.send(f"Please select a target for [Murder]")
                if game.canUseSubstitution == True:
                    await personRoom.send(f"Will you change roles with The Double?")
            
            
            if j.getClass() == "Prince":
                classes = [classes.gameClass for classes in game.getListPlayers()]
                if j == game.getMurderUser():
                    await personRoom.send(f"Please select a target for [Murder]")
                else:
                    await personRoom.send(f"Murder unavailable")
            if j.getClass() == "Double":
                classes = [classes.gameClass for classes in game.getListPlayers()]
                if j == game.getMurderUser():
                    await personRoom.send(f"Please select a target for [Murder]")
                else:
                    await personRoom.send(f"Murder unavailable")

        await asyncio.sleep(game.sleepTimeTable)
        
    
        await game.makeSecretMeeting()
        await asyncio.sleep(5)
        
        for j in game.actions:
            await j.__anext__()
            await j.__anext__()
        game.actions.clear()

        game.currentBlock = "D"
        serial = jsonpickle.encode(game)
        jsonLogger(serial)
        await bigRoomC.send(f"{game.getDays()[i]} Day <D> Big room")
        for j in game.getListPlayers():
            j.choosedPartner = False
            await j.getID().move_to(bigRoomV)

        await cancelableSleep(game.sleepBigRoom, game.cond, game)
        game.bigRoomSkip = 0
        game.currentBlock = "E"
        serial = jsonpickle.encode(game)
        jsonLogger(serial)
        await game.bigRoomC.set_permissions(game.guild.default_role, read_messages=False)
        await bigRoomC.send(f"{game.getDays()[i]} Day <E> owns's room")

        for j in game.getListPlayers():
            j.skipped = False
            personRoom = game.getPrivateTextChannel(j.name)
            await personRoom.send(f"{game.getDays()[i]} Day <E> [{j.name}]'s room")
            if j.getClass() == "Revolutionary":
                await personRoom.send(f"Please select a target for [Assassination]")
            await j.getID().move_to(j.getPrivateVoiceChannel())
        
        await asyncio.sleep(game.sleepTimeTable + 10)
        for j in game.actions:
            await j.__anext__()
            await j.__anext__()
        i += 1
        game.actions.clear()
        
        game.murderTarget = None
        game.substitutionUsed = False
        await game.bigRoomC.set_permissions(game.guild.default_role, read_messages=True)
        if i == 7:
            if len(game.listPlayers) == 6:
                for j in game.listPlayers:
                    if j.isPlayer == True:
                        j.score = 0
                        j.diedAsPlayer = True
                    else:
                        j.score += 1
            else:
                for j in game.listPlayers:
                    if j.isPlayer == True:
                        j.score = 0
                        j.diedAsPlayer = True

async def timeTable (ctx, game : KingdomRoyale):
    for k in range(6):
        game.cond = asyncio.Condition()
        if k != 0:
            await game.turnReset()
            
            game.setPlayer()
        game.taskTurn = asyncio.create_task(turnLoop(ctx, game))
        try:
            await game.taskTurn
        except:
            print("fodasse")


