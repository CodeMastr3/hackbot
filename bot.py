import discord
import discord.utils
import emojiRole
import token1
import ast
from datetime import datetime
from random import seed
from random import randint
from discord.ext import commands

seed(datetime.now())

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    "Returns pong"
    await ctx.send('pong')

messageDict = emojiRole.message

watched_message = {}

with open('dict.txt', 'r') as f:
    s = f.read()
    if not s:
        pass
    else:
        watched_message = ast.literal_eval(s)

emojiList = {}

@bot.command()
async def addMessage(ctx):
    "Adds the Role Messages"
    global messageDict
    global watched_message
    global emojiList
    for mess,emolist in messageDict.items():
        reacted_message = await ctx.send(mess)
        watched_message[reacted_message.id] = emolist
        f = open("dict.txt", "w")
        f.write(str(watched_message))
        f.close()
        for emo in emolist:
            await reacted_message.add_reaction(emo)

@bot.command(pass_context=True)
async def roll(ctx, arg1=1, arg2=100):
    "You can specify the amount of type of dice with a space, else it will be a random num between 1-100"
    author = ctx.message.author
    for i in range(arg1):
        randomNumber = randint(1, arg2)
        await ctx.send('%s rolled a %d' % (author, randomNumber))

@bot.command()
async def logout(ctx):
    "Logs the bot out"
    await bot.logout()

async def manage_reactions( payload, added: bool):
    if not payload.message_id in watched_message:
        return

    messageID = payload.message_id
    mapping = watched_message[messageID]

    if not payload.emoji.name in mapping:
    # reaction.emoji is str if normal emoji or ID if custom, but we use both as keys in mapping
        print("Hello")
        return
    
    guildName = bot.get_guild(payload.guild_id)
    member = discord.utils.get(guildName.members, id=payload.user_id)
    print(member)
    role = discord.utils.get(guildName.roles, name=mapping[payload.emoji.name])
    print(role)

    if added:
        await member.add_roles(role)
    else:
        await member.remove_roles(role)

@bot.event
async def on_raw_reaction_add(payload):
    print("Hi")
    await manage_reactions(payload, True)

@bot.event
async def on_raw_reaction_remove(payload):
    await manage_reactions(payload, False)

bot.run(token1.stringToken())
