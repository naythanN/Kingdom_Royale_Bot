import discord
from discord.ext import commands
import os

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
	for i in game.privateChannels:
		await i.delete()
	for i in game.secretMeetings:
		await i.delete()
	await game.bigRoom.delete()
	game.__init__()


@client.command(name = "set")
async def reg (ctx):
	pass


@client.command(name = "reg")
async def reg (ctx):
	game.addPlayer(ctx.message.author.name)
	

	
@client.command(name = "start")
async def reg (ctx):
	guild = ctx.message.guild
	for i in game.listPlayers:
		overwrites = {
			guild.default_role : discord.PermissionOverwrite(read_messages=False),
			guild.me: discord.PermissionOverwrite(read_messages=True)
		}
		game.setPrivateChannel(await guild.create_text_channel(i.name + "'s room", overwrites = overwrites), i.name)
	for i in range(len(game.listPlayers)):
		game.setSecretMeetings (await guild.create_voice_channel("Meeting Room " + str(i)))
	game.setBigRoom (await guild.create_voice_channel("Big Room"))



client.run(token)

