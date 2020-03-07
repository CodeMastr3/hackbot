import discord
import discord.utils
import emojiRole
import token1
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

messageDict = emojiRole.message

watched_message = {}
emojiList = {}

@bot.command()
async def addMessage(ctx):
    global messageDict
    global watched_message
    global emojiList
    for mess,emolist in messageDict.items():
        reacted_message = await ctx.send(mess)
        watched_message[reacted_message.id] = emolist
        for emo in emolist:
            await reacted_message.add_reaction(emo)
    #reacted_message = await ctx.send("Hi")
    
    #emoji = '\N{THUMBS UP SIGN}'
    #emojiList[emoji] = '685902355404947535'
    #emoji = '\U0001F600'#U0001F44D'
    #emojiList[emoji] = 'test'
    
    #watched_message[reacted_message.id] = emojiList
    #await reacted_message.add_reaction(emoji)

@bot.command()
async def logout(ctx):
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
