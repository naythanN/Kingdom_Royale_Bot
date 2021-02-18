import discord
from discord.ext import commands
import os
import asyncio


from player import Player
from kingdomRoyale import KingdomRoyale

client = commands.Bot(command_prefix="/")
token = os.getenv("DISCORD_BOT_TOKEN")
print(token)

game = KingdomRoyale ()


@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to .help"))
    print("I am online")




@client.command()
async def clear(ctx, amount=3) :
    await ctx.channel.purge(limit=amount)

@client.command(name = "reset")
async def reset (ctx):
	thisServer = ctx.message.guild
	for i in game.getAllPrivateTextChannels():
		await i.delete()
	for i in game.getAllPrivateVoiceChannels():
		await i.delete()
	await game.getBigRoomChat().delete()
	await game.getBigRoomVoice().delete()
	game.taskTimeTable.cancel()
	game.__init__()


@client.command(name = "Sorcery")
async def reg (ctx):
	player = ctx.message.author
	for i in game.getListPlayers():
		if i.getID() == player and i.getClass() == "Sorcerer":
			game.sorcery(i)
			return
	game.getPrivateTextChannel(player.name).send("Sorcery unavaiable")

@client.command(name = "Deathblow")
async def reg (ctx):
	player = ctx.message.author
	for i in game.getListPlayers():
		if i.getID() == player and i.getClass() == "Knight":
			game.deathblow(i)
			return
	game.getPrivateTextChannel(player.name).send("Deathblow unavaiable")

@client.command(name = "Murder")
async def reg (ctx, target):
	player = ctx.message.author
	for i in game.getListPlayers():
		if i.getID() == player and i == game.getMurderUser():
			game.murder(target)
			return
	game.getPrivateTextChannel(player.name).send("Murder unavaiable")

@client.command(name = "Substitution")
async def reg (ctx):
	player = ctx.message.author
	for i in game.getListPlayers():
		if i.getID() == player and i.getClass() == "King":
			game.sorcery()
			return
	game.getPrivateTextChannel(player.name).send("Substitution unavaiable")

@client.command(name = "Assassination")
async def reg (ctx, target):
	player = ctx.message.author
	for i in game.getListPlayers():
		if i.getID() == player and i.getClass() == "Revolutionary":
			game.assassination(target)
			return
	game.getPrivateTextChannel(player.name).send("Sorcery unavaiable")

@client.command(name = "reg")
async def reg (ctx):
	game.addPlayer(ctx.message.author)

@client.command(name = "choose")
async def reg (ctx, target):
	game.addPlayer(ctx.message.author)
	player = ctx.message.author

@client.command(name = "class")
async def reg (ctx, gameClass):


	player = ctx.message.author
	for i in game.getListPlayers():
		if i.member == player and i.gameClass == None:
			if gameClass == None:
				game.getPrivateTextChannel(i.name).send("Choose a class")
				return
			if gameClass not in game.avaiableClasses:
				game.getPrivateTextChannel(i.name).send("Wrong Class name")
				return
			if i.isPlayer == False:
				game.getPrivateTextChannel(i.name).send("You can't choose your class")
				return
			pastClasses = [classes.gameClass for classes in game.pastPlayers]
			if gameClass in pastClasses:
				game.getPrivateTextChannel(i.name).send("Class already choosen before")
				return
			i.setClass(gameClass)
			game.classToPick.remove(gameClass)



	
@client.command(name = "start")
async def reg (ctx):
	guild = ctx.message.guild
	for i in game.getListPlayers():
		overwrites = {
			guild.default_role : discord.PermissionOverwrite(read_messages=False),
			guild.me: discord.PermissionOverwrite(read_messages=True)
		}
		game.setPrivateTextChannel(await guild.create_text_channel(i.name + "'s room", overwrites = overwrites), i.name)
		game.setPrivateVoiceChannel(await guild.create_voice_channel(i.name + "'s room", overwrites = overwrites), i.name)

	game.setBigRoomV (await guild.create_voice_channel("Big Room"))
	game.setBigRoomC (await guild.create_text_channel("Big Room"))
	game.setPlayer()


	game.taskTimeTable = asyncio.create_task (timeTable (ctx))
	


async def timeTable (ctx):
	await ctx.send("Welcome to Kingdom Royale! Hehe")
	for i in range(6):
		if i != 0:
			game.turnReset()
			game.setPlayer()
		for i in range(7):
			bigRoomC = game.getBigRoomChat()
			bigRoomV = game.getBigRoomVoice()
			await bigRoomC.send(f"{game.getDays()[i]} Day <A> owns's room")
			
			for j in game.getListPlayers():
				personRoom = game.getPrivateTextChannel(j.name)
				await personRoom.send(f"{game.getDays()[i]} Day <A> [{j.name}]'s room")
				if j.isPlayer == True and i == 0:
					await personRoom.send(f"Gufufu - PleaSed to - meEt you - {j.name}-kun - Alright - you wiLl now - select yOur [class]")
				await j.getID().move_to(j.getPrivateVoiceChannel())

			await asyncio.sleep(10)
			await bigRoomC.send(f"{game.getDays()[i]} Day <B> Big room")
			for j in game.getListPlayers():
				await j.getID().move_to(bigRoomV)
			await asyncio.sleep(10)
			await bigRoomC.send(f"{game.getDays()[i]} Day <C> owns's room")
			if i == 0:
				game.setClasses()
				for j in game.getListPlayers():
					personRoom = game.getPrivateTextChannel(j.name)
					await personRoom.send(f"Your [class] is [{j.gameClass}]")

			for j in game.getListPlayers():
				personRoom = game.getPrivateTextChannel(j.name)
				if j.getClass() == "Sorcerer":
					if game.murderTarget is None:
						await personRoom.send(f"No target has been selected for [Murder] yet.")
					else:
						await personRoom.send(f"Will you burn [{game.murderTarget.getName()}] to death by using [Sorcery]?")
				if j.getClass() == "Knight":
					classes = [classes.gameClass for classes in game.getListPlayers()]
					#if "Sorcerer" in classes:
				#		await personRoom.send(f"No target has been selected for [Murder] yet.")
					if game.murderTarget is None and "Sorcerer" not in classes:
						await personRoom.send(f"No target has been selected for [Murder] yet.")
					elif game.murderTarget is not None and "Sorcerer" not in classes:
						await personRoom.send(f"Do you want to kill [{game.murderTarget.getName()}] by using [Deathblow]?")
				if j.getClass() == "King":
					if j == game.getMurderUser():
						await personRoom.send(f"Please select a target for [Murder]")
					await personRoom.send(f"Will you change roles with The Double?")
				
				
				if j.getClass() == "Prince":
					classes = [classes.gameClass for classes in game.getListPlayers()]
					if j == game.getMurderUser():
						await personRoom.send(f"Please select a target for [Murder]")
					else:
						await personRoom.send(f"Murder unavaiable")
				if j.getClass() == "Double":
					classes = [classes.gameClass for classes in game.getListPlayers()]
					if j == game.getMurderUser():
						await personRoom.send(f"Please select a target for [Murder]")
					else:
						await personRoom.send(f"Murder unavaiable")

				await j.getID().move_to(j.getPrivateVoiceChannel())
			await asyncio.sleep(10)

			await bigRoomC.send(f"{game.getDays()[i]} Day <D> Big room")
			for j in game.getListPlayers():
				await j.getID().move_to(bigRoomV)

			await asyncio.sleep(10)

			await bigRoomC.send(f"{game.getDays()[i]} Day <E> owns's room")

			for j in game.getListPlayers():
				personRoom = game.getPrivateTextChannel(j.name)
				await personRoom.send(f"{game.getDays()[i]} Day <E> [{j.name}]'s room")
				if j.getClass() == "Revolutionary":
					await personRoom.send(f"Please select a target for [Assassination]")
				await j.getID().move_to(j.getPrivateVoiceChannel())
			
			await asyncio.sleep(10)


client.run(token)

