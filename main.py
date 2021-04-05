import discord
from discord.ext import commands
import os
import asyncio
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option

from player import Player
from kingdomRoyale import KingdomRoyale, SecretMeeting

from table import timeTable


client = commands.Bot(command_prefix="/",intents=discord.Intents.all())
#client = discord.Client(intents=discord.Intents.all())

token = os.getenv("DISCORD_BOT_TOKEN")
guilds = [802152034484617236, 824649618079350815]

game = KingdomRoyale ()


slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready() :
    #await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to .help"))
    print("I am online")


@slash.slash(name="skip", guild_ids=guilds,
             description="Vote to skip current block if its a secret meeting or a big room")
async def skip(ctx):
    author = ctx.message.author
    player = [i for i in game.listPlayers if i.getID() == author][0]
    print(player)
    if game.currentBlock == "C":
        for i in game.secretMeetings:
            if player in {i.other, i.whoRoom} and player.skipped == False and player.occupied == True:
                i.skip += 1
                player.skipped = True
                if i.skip == 2:
                    await i.cond.acquire()
                    i.cond.notify()
                    i.cond.release()

    elif game.currentBlock in {"B", "D"}:
        if player.skipped == False:
            game.bigRoomSkip += 1
            player.skipped = True
            if game.bigRoomSkip == len(game.getListPlayers()):
                await game.cond.acquire()
                game.cond.notify()
                game.cond.release()

    else:
        ctx.send("There is nothing to skip")



@client.command(name = "cleanMess")
async def cleanMess (ctx):
    thisServer = ctx.message.guild
    for i in thisServer.channels:
        await i.delete()
    await thisServer.create_voice_channel("Main")
    await thisServer.create_text_channel("Main")
    game.__init__()


@slash.slash(name="help", guild_ids=guilds,
             description="Vote to skip current block")
async def helpMe (ctx):
    helpBot = "Welcome to the Kingdom Royale Bot, a discord bot that implements the game of the same name based on Eiji Mikaje light novel, Utsuro no hako to zero no Maria.\n Avaiable commands:\n /reg register yourself to play the game.\n /start Start the game with current registered players. \n /choose [member_name] Choose a player of the game as partner for secreet meeting (if name has spaces, quote it with \"\").\n /classC [class_name one of King, Sorcerer, Knight, Prince, Double, Revolutionary] If you are the [Player] you can choose your class. \n /Murder [member_name] If you are able to select, you can choose someone to be marked to die.\n /Assassination [member_name] If you are the revolutionary, you can select someone to die.\n /Sorcery If you are the sorcerer, you burn the one marked to death.\n /Deathblow If you are the knight you can kill the one marked if the sorcerer is dead.\n /Substitution If you are the King you can prevent being killed by assassination changing roles with the Double. \n /Strike [member_name] You can strike someone with your knife.\n /cleanMess to clean the server. \n /reset to reset the game."
    await ctx.send(helpBot)



@slash.slash(name="Strike", guild_ids=guilds,
             description="Stab someone",options=[
                    create_option(
                    name="target",
                    description="Select target to stab",
                    option_type=6,
                    required=True
                )
                ])
async def Strike (ctx, target):
    player = ctx.message.author
    for i in game.getListPlayers():
        if i.getID() == player and game.canStrike(i, game.getPlayer(target)):
            if game.getPlayer(target) is not None:
                i.strike = False
                await game.strike(i, target)
                return
            else:
                await i.getID().send("The target does not exist or is already dead.")
    await game.getPrivateTextChannel(player.name).send("Strike unavailable")



@slash.slash(name="Sorcery", guild_ids=guilds,
             description="Confirm death request from [Murder] user",options=[
                    create_option(
                    name="target",
                    description="Select target to become a burnt corpse",
                    option_type=6,
                    required=True
                )
                ])
async def Sorcery (ctx):
    player = ctx.message.author
    for i in game.getListPlayers():
        if i.getID() == player and i.getClass() == "Sorcerer" and game.currentBlock == "C":
            if game.murderTarget is not None and (game.murderTarget.pair != i or i.isPlayer == True):
                game.actions.append(game.sorcery(i))
                return                
            elif game.murderTarget is not None and game.murderTarget.pair == i and i.isPlayer == False:
                await i.getPrivateTextChannel().send("This is your dear friend you have known forever, you cannot bring yourself to kill him.")

    await game.getPrivateTextChannel(player.name).send("Sorcery unavailable")


@slash.slash(name="Deathblow", guild_ids=guilds,
             description="Confirm death request from [Murder] user",options=[
                    create_option(
                    name="target",
                    description="Select target to die by beheading",
                    option_type=6,
                    required=True
                )
                ])
async def Deathblow (ctx):
    player = ctx.message.author
    for i in game.getListPlayers():
        if i.getID() == player and i.getClass() == "Knight" and game.currentBlock == "C":
            if game.murderTarget is not None and (game.murderTarget.pair != i or i.isPlayer == True):
                game.actions.append(game.deathblow(i))
                return
                
            elif game.murderTarget is not None and game.murderTarget.pair == i and i.isPlayer == False:
                i.getPrivateTextChannel().send("This is your dear friend you have known forever, you cannot bring yourself to kill him.")
    await game.getPrivateTextChannel(player.name).send("Deathblow unavailable")


@slash.slash(name="Murder", guild_ids=guilds,
                description="Select a target for [Murder]",options=[
                    create_option(
                    name="target",
                    description="Target to be marked by [Murder]",
                    option_type=6,
                    required=True
                )
                ]
                )
async def Murder (ctx, target):
    player = ctx.message.author
    for i in game.getListPlayers():
        if i.getID() == player and i == game.getMurderUser() and game.currentBlock == "C":
            if game.getPlayer(target) is not None:
                if game.getPlayer(target).pair == i and i.isPlayer == False:
                    await i.getPrivateTextChannel().send("This is your dear friend you have known forever, you can'nt bring yourself to kill him.")
                else:
                    await game.murder(target)
                    return
            else:
                await i.getID().send("The target does not exist or is already dead.")
    await game.getPrivateTextChannel(player.name).send("Murder unavailable")



@slash.slash(name="Substitution", guild_ids=guilds,
             description="The King will change roles with the Double")
async def Substitution (ctx):
    player = ctx.message.author
    for i in game.getListPlayers():
        if i.getID() == player and i.getClass() == "King" and game.canUseSubstitution == True and game.currentBlock == "C":
            game.substitution()
            await game.getPlayer("Double").getPrivateTextChannel().send(f"Please select a target for [Murder]")
            return
    await game.getPrivateTextChannel(player.name).send("Substitution unavailable")



@slash.slash(name="Assassination", guild_ids=guilds,
                description="Select a target for [Assassination]",options=[
                    create_option(
                    name="target",
                    description="Target to die",
                    option_type=6,
                    required=True
                )
                ]
                )
async def Assassination (ctx, target):
    player = ctx.message.author
    for i in game.getListPlayers():
        if i.getID() == player and i.getClass() == "Revolutionary" and game.currentBlock == "E":
            if game.getPlayer(target) is not None:
                if game.getPlayer(target).pair == i and i.isPlayer == False:
                    await i.getPrivateTextChannel().send("This is your dear friend you have known forever, you can'nt bring yourself to kill him.")
                else:
                    game.actions.append(game.assassination(target))
                    return
            else:
                await i.getID().send("The target does not exist or is already dead.")
    await game.getPrivateTextChannel(player.name).send("Assassination unavailable")



@slash.slash(name="reg", guild_ids=guilds,
             description="Register yourself to participate in the game")
async def reg (ctx):
    members = [i.member for i in game.listPlayers]
    if ctx.message.author not in members:
        game.addPlayer(ctx.message.author)
    else:
        await ctx.send("Already registered")



@slash.slash(name="mode", guild_ids=guilds,
             description="Change game mode, default=Pairs",
             options=[
                 create_option(
                     name="gameMode",
                     description="Select gameMode",
                     option_type=3,
                     required=True,
                     choices=[
                         create_choice(
                             name="Solo",
                             value="Solo"
                         ),
                         create_choice(
                             name="Pairs",
                             value="Pairs"
                         )
                     ]
                 )
             ])
async def mode (ctx, gameMode: str):
    if gameMode == "Solo" or gameMode == "Pairs":
        game.mode = gameMode 
    else:
        await ctx.send("Unavaible game mode")

@slash.slash(name="choose", guild_ids=guilds,
                description="Select a partner for Secret Meeting",options=[
                    create_option(
                    name="target",
                    description="Partner",
                    option_type=6,
                    required=True
                )
                ]
                )
async def choose (ctx, target):
    
    player = ctx.message.author

    playerChooser = [players for players in game.getListPlayers() if players.name == player.name][0]
    playerChosen = [players for players in game.getListPlayers() if players.name == target][0]

    toDouble = [players.other for players in game.secretMeetings if players.whoRoom == playerChosen]

    if len(toDouble) != 0 and toDouble[0] == playerChooser:
        secret = [secret for secret in game.secretMeetings if secret.whoRoom == playerChosen]
        if len(secret) != 0:
            secret[0].double()
    else:
        secret = SecretMeeting(playerChooser, playerChosen)
        game.secretMeetings.append(secret)

@slash.slash(name="class", guild_ids=guilds,
             description="Select your class if you are the [Player]",
             options=[
                 create_option(
                     name="gameClass",
                     description="Select class",
                     option_type=3,
                     required=True,
                     choices=[
                         create_choice(
                             name= "King",
                             value="King"
                         ),
                         create_choice(
                             name= "Prince",
                             value="Prince"
                         ),
                         create_choice(
                             name= "Double",
                             value="Double"
                         ),
                         create_choice(
                             name= "Knight",
                             value="Knight"
                         ),
                         create_choice(
                             name= "Sorcerer",
                             value="Sorcerer"
                         ),
                         create_choice(
                             name= "Revolutionary",
                             value="Revolutionary"
                         )
                     ]
                 )
             ])
async def classC (ctx, gameClass):

    player = ctx.message.author
    for i in game.getListPlayers():
        if i.member == player and i.gameClass == None:
            if gameClass == None:
                await game.getPrivateTextChannel(i.name).send("Choose a class")
                return
            if gameClass not in game.avaiableClasses:
                await game.getPrivateTextChannel(i.name).send("Wrong Class name")
                return
            if i.isPlayer == False:
                await game.getPrivateTextChannel(i.name).send("You can't choose your class")
                return
            pastClasses = [classes.gameClass for classes in game.pastPlayers]
            if gameClass in pastClasses:
                await game.getPrivateTextChannel(i.name).send("Class already choosen before")
                return
            i.setClass(gameClass)
            game.classToPick.remove(gameClass)
            game.cond.acquire()
            game.cond.notify()
            game.cond.release()



@slash.slash(name="start", guild_ids=guilds,
             description="Start Kingdom Royale")
async def start (ctx):
    if game.gameStarted == True:
        await ctx.send("Game already started")
        return
    game.gameStarted = True
    guild = ctx.message.guild
    game.guild = guild
    for i in game.getListPlayers():
        overwrites = {
            guild.default_role : discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        await game.setPrivateTextChannel(await guild.create_text_channel(i.name + "'s room", overwrites = overwrites), i.name)

        await game.setPrivateVoiceChannel(await guild.create_voice_channel(i.name + "'s room", overwrites = overwrites), i.name)

    game.setBigRoomV (await guild.create_voice_channel("Big Room"))
    game.setBigRoomC (await guild.create_text_channel("Big Room"))
    game.graveyard = await guild.create_voice_channel("Graveyard")
    game.setPlayer()


    game.taskTimeTable = asyncio.create_task (timeTable (ctx, game))


client.run(token)



