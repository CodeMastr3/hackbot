import discord
import discord.utils
import emojiRole
import token1 as token
import ast
import requests

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

@bot.command(hidden=True)
async def secret(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete()

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
    member = ctx.author
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
async def poll(ctx, *arg):
    "Adds (a) reaction(s) to a poll message with the number immediately after poll"
    for i in range(arg1):
        ctx.send('I\'m not implemented yet')
        #
        #await ctx.message.add_reaction('\U0001F3B2')
"""

@bot.command()
async def joined(ctx):
    "Tells you when you joined the server using UTC"
    member = ctx.author
    await ctx.send('Time %s joined %s in UTC:\n%s' %(member.mention, ctx.guild.name, member.joined_at))

@bot.command(pass_context=True)
async def roll(ctx, arg1="1", arg2="100"):
    "You can specify the amount of dice with a space or delimited with a 'd', else it will be 2 random nums between 1-6"
    await ctx.message.add_reaction('\U0001F3B2')
    author = ctx.message.author.display_name
    sum_dice = 0
    message = ""
    arg1 = str(arg1).lower()

    if("d" in arg1):
        arg1, arg2 = arg1.split("d", 1)
        if(arg1 == ""):
            arg1 = "1"
        if(arg2 == ""):
            await ctx.send(f"Woah {author}, your rolls are too powerful")
            return;

    if(not arg1.isdecimal() or not str(arg2).isdecimal()):
        await ctx.send(f"Woah {author}, your rolls are too powerful")
        return

    arg1 = int(arg1)
    arg2 = int(arg2)

    if(arg1 > 100 or arg2 > 100):
        await ctx.send(f"Woah {author}, your rolls are too powerful")
        return
    elif arg1 < 1 or arg2 < 1:
        await ctx.send(f"Woah {author}, your rolls are not powerful enough")
        return

    # Is it possible to be *too* pythonic?
    message += (f"{author} rolled {arg1} d{arg2}{(chr(39) + 's') if arg1 != 1 else ''}\n")
    # Never.

    message += ("\n")
    for i in range(1, arg1+1):
        roll = randint(1, arg2)
        sum_dice += roll
        if(arg2 == 20 and roll == 20):
            message += (f"Roll {i}: {roll} - Critical Success! (20)\n")
        elif(arg2 == 20 and roll == 1):
            message += (f"Roll {i}: {roll} - Critical Failure! (1)\n")
        else:
            message += (f"Roll {i}: {roll}\n")

    message += ("\n")
    message += (f"Sum of all rolls: {sum_dice}\n")
    if(len(message) >= 2000):
        await ctx.send(f"Woah {author}, your rolls are too powerful")
    else:
        await ctx.send(message)

@bot.command(hidden=True)
@commands.has_any_role('Cody', 'Dallas')
async def logout(ctx):
    "Logs the bot out"
    await bot.logout()

@bot.command()
async def escalate(ctx):
    await ctx.send('ESCALATING')

def normalize_location(loc):
    """
    Used by vaccines command:
    Will change a phrase like "uNITED sTATES" to "United States" since all location are stored as proper nouns
    """
    arr = [i.lower() for i in loc.split(' ')]
    arr =[''.join([word[i] if i != 0 else word[i].upper() for i in range(len(word))]) for word in arr]
    return ' '.join(arr)

def gll(js, loc):
    """
    Used for the vaccines command, will find the first information
    based off the country.
    """
    for s in js[::-1]:
        if s['location'] == loc:
            return s
    return None


@bot.command()
async def vaccines(ctx, loc = "United States"):
    """
    Uses the information available at howmanyvaccinated.com to state how many people have been vaccinated based off location
    Will default to United States
    """
    url = "https://www.howmanyvaccinated.com/vaccine"
    page = requests.get(url);
    js = page.json()

    #Make sure that the location has every chance to succeed without fuzzy finding
    loc = normalize_location(loc)
    dat = gll(js,loc)
    msg = ""
    if dat is not None:
        #Format the number with commas to make it easier to read
        tot = "{:,}".format(int(dat['total_vaccinations']))
        msg = f"In {loc} as of {dat['date']}, there have been {tot} vaccinations, totalling {dat['total_vaccinations_per_hundred']}% of the population."
    else:
        msg = f"Unable to find information for {loc}"
    await ctx.send(msg)


@logout.error
async def logout_error(ctx, error):
    await ctx.channel.send("You don't have the permission to run that command")

@bot.command(pass_context=True)
async def sub(ctx, *args):
    "Subtracts any roles mentioned after sub if they exist say all for all possible roles to remove"
    member = ctx.author
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
    await ctx.send('I\'ve removed your requested roles %s!' %member.mention)

@sub.error
async def sub_error(ctx, error):
    await ctx.channel.send("You have probably typed a role that doesn't exist please make sure that isn't the case and try again")

@bot.command(pass_context=True)
async def add(ctx, *args):
    "Adds any roles mentioned after add if they exist say all for all roles possible to add"
    member = ctx.author
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
    await ctx.send('I\'ve added your new roles %s!' %member.mention)

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
async def on_member_join(member):
    botChannel = discord.utils.get(member.guild.channels, name='bot-stuff')
    rulesChannel = discord.utils.get(member.guild.channels, name='rules-and-info')
    await botChannel.send('Welcome to the server %s!\nPlease check out %s!\nIn order to view channels you need to add the relevant roles. Type !help for help, !serverroles for the roles you can add yourself to, !add "role1" "role2" to put yourself in that course.' %(member.mention, rulesChannel.mention))

@bot.event
async def on_raw_reaction_add(payload):
    await manage_reactions(payload, True)

@bot.event
async def on_raw_reaction_remove(payload):
    await manage_reactions(payload, False)

bot.run(token.stringToken())
