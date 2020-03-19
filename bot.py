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

@bot.command()
async def say(ctx, *, arg):
    "Says what you put"
    await ctx.send(arg)

messageDict = emojiRole.message
with open('roles.txt', 'r') as f:
    s = f.read()
    if not s:
        pass
    else:
        messageDict = ast.literal_eval(s.replace("\\\\", "\\"))

watched_message = {}

with open('dict.txt', 'r') as f:
    s = f.read()
    if not s:
        pass
    else:
        watched_message = ast.literal_eval(s)

emojiList = {}

@bot.command()
@commands.has_any_role('Cody', 'Dallas')
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

@bot.command()
async def myroles(ctx):
    "Lists roles of member that called this function"
    member = discord.utils.get(ctx.guild.members, name=ctx.author.name)
    s = ""
    iterroles = iter(member.roles)
    next(iterroles)
    for role in iterroles:
        s+=role.name
        s+="\n"
    await ctx.send('Your roles:\n%s' %s)

@bot.command()
async def serverroles(ctx):
    "Lists roles of the server"
    s = ""
    roles = ctx.guild.roles
    iterroles = iter(roles)
    next(iterroles)
    for role in iterroles:
        if role.name == "hackbot 1.1":
            break
        else:
            s+=role.name
            s+="\n"
    await ctx.send('Servers roles:\n%s' %s)

"""
@bot.command()
async def poll(ctx, arg1):
    "Adds a reactions to a poll message with the number immediately after poll"
    for i in range(arg1):
        ctx.send('I\'m not implemented yet')
        #
        #await ctx.message.add_reaction('\U0001F3B2')
"""
@bot.command()
async def joined(ctx):
    "Tells you when you joined the server using UTC"
    member = discord.utils.get(ctx.guild.members, name=ctx.author.name)
    await ctx.send('Time you joined %s in UTC:\n%s' %(ctx.guild.name, member.joined_at))


@bot.command(pass_context=True)
async def roll(ctx, arg1=1, arg2=100):
    "You can specify the amount of type of dice with a space, else it will be a random num between 1-100"
    author = ctx.message.author
    message = ""
    summ = 0
    for i in range(arg1):
        num = randint(1, arg2)
        summ += num
        message += f"Roll {i}: {num}\n"
    message = f"{author} rolled:\n{message}\nWith a sum of:{summ}"
    if(len(message) >= 2000):
        await ctx.send('Woah %s, your rolls are too powerful' % (author))
    else:
        await ctx.send('%s' % (message))
    await ctx.message.add_reaction('\U0001F3B2')

@bot.command()
@commands.has_any_role('Cody', 'Dallas')
async def logout(ctx):
    "Logs the bot out"
    await bot.logout()

@bot.command()
async def escalate(ctx):
    await ctx.send('ESCALATING')

@logout.error
async def sub_error(ctx, error):
    await ctx.channel.send("You don't have the permission to run that command")

@bot.command(pass_context=True)
async def sub(ctx, *args):
    "Subtracts any roles mentioned after sub if they exist say all for all possible roles to remove"
    member = discord.utils.get(ctx.guild.members, name=ctx.author.name)
    for arg in args:
        if(arg == "all"):
            roles = ctx.guild.roles
            iterroles = iter(roles)
            next(iterroles)
            for role in iterroles:
                if role.name == "hackbot 1.1":
                    break
                else:
                    await member.remove_roles(role)
            break
        else:
            role = discord.utils.get(ctx.guild.roles, name=arg)
            await member.remove_roles(role)
    await ctx.send('I\'ve removed your requested roles %s!' %ctx.author.name)

@sub.error
async def sub_error(ctx, error):
    await ctx.channel.send("You have probably typed a role that doesn't exist please make sure that isn't the case and try again")

@bot.command(pass_context=True)
async def add(ctx, *args):
    "Adds any roles mentioned after add if they exist say all for all roles possible to add"
    member = discord.utils.get(ctx.guild.members, name=ctx.author.name)
    for arg in args:
        if(arg == "all"):
            roles = ctx.guild.roles
            iterroles = iter(roles)
            next(iterroles)
            for role in iterroles:
                if role.name == "hackbot 1.1":
                    break
                else:
                    await member.add_roles(role)
            break
        else:
            role = discord.utils.get(ctx.guild.roles, name=arg)
            await member.add_roles(role)
    await ctx.send('I\'ve added your new roles %s!' %ctx.author.name)

@add.error
async def add_error(ctx, error):
    await ctx.channel.send("You have probably typed a role that doesn't exist please make sure that isn't the case and try again")

async def manage_reactions(payload, added: bool):
    if not payload.message_id in watched_message:
        return

    messageID = payload.message_id
    mapping = watched_message[messageID]

    if not payload.emoji.name in mapping:
    # reaction.emoji is str if normal emoji or ID if custom, but we use both as keys in mapping
        return
    
    guildName = bot.get_guild(payload.guild_id)
    member = discord.utils.get(guildName.members, id=payload.user_id)
    role = discord.utils.get(guildName.roles, name=mapping[payload.emoji.name])

    if added:
        await member.add_roles(role)
    else:
        await member.remove_roles(role)

@bot.event
async def on_raw_reaction_add(payload):
    await manage_reactions(payload, True)

@bot.event
async def on_raw_reaction_remove(payload):
    await manage_reactions(payload, False)

bot.run(token1.stringToken())

