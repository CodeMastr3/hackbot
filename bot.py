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
async def roll(ctx):
  randomNumber = randint(1, 100)
  author = ctx.message.author
  await ctx.send('%s rolled a %d' % (author, randomNumber))

@bot.command()
async def logout(ctx):
    "Logs the bot out"
    await bot.logout()

async def manage_reactions(reaction, user, added: bool):
    if not reaction.message.id in watched_message:#self.watched_message:
        return

    messageID = reaction.message.id
    mapping = watched_message[messageID]

    if not reaction.emoji in mapping:
    # reaction.emoji is str if normal emoji or ID if custom, but we use both as keys in mapping
        return

    member = discord.utils.get(reaction.message.guild.members, id=user.id)

    role = discord.utils.get(reaction.message.guild.roles, name=mapping[reaction.emoji])

    if added:
        await member.add_roles(role)
    else:
        await member.remove_roles(role)

@bot.event
async def on_reaction_add(reaction, user):
    await manage_reactions(reaction, user, True)

@bot.event
async def on_reaction_remove(reaction, user):
    await manage_reactions(reaction, user, False)

bot.run(token1.stringToken())
