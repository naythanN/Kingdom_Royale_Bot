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
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")


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



@client.command(name = "reg")
async def reg (ctx):
	game.addPlayer(ctx.message.author)
	

	
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

	game.taskTimeTable = asyncio.create_task (timeTable (ctx))
	


async def timeTable (ctx):
	await ctx.send("Welcome to Kingdom Royale! Hehe")
	for i in range(7):
		bigRoomC = game.getBigRoomChat()
		bigRoomV = game.getBigRoomVoice()
		await bigRoomC.send(f"{game.getDays()[i]} Day <A> owns's room")
		
		for j in game.getListPlayers():
			personRoom = game.getPrivateTextChannel(j.name)
			await personRoom.send(f"{game.getDays()[i]} Day <A> [{j.name}]'s room")
			await j.getID().move_to(j.getPrivateVoiceChannel())

		await asyncio.sleep(10)
		await bigRoomC.send(f"{game.getDays()[i]} Day <B> Big room")
		for j in game.getListPlayers():
			await j.getID().move_to(bigRoomV)
		await asyncio.sleep(10)
		await bigRoomC.send(f"{game.getDays()[i]} Day <C> owns's room")
		for j in game.getListPlayers():
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
			await j.getID().move_to(j.getPrivateVoiceChannel())
		
		await asyncio.sleep(10)


client.run(token)

