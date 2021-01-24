import discord
import discord.utils
import emojiRole
import token1 as token
import ast
import requests
import subprocess
#import os
import json

import time
from datetime import datetime
# from dotenv import load_dotenv
from random import seed
from random import randint
from random import choice
from discord.ext import commands

seed(datetime.now())
start_time = time.time()
# load_dotenv('.env')

#Load json data
json_file = "db.json"
json_db = {}
#If file doesn't exist, screw it, we'll write it later
try:
    with open(json_file, 'r') as f:
        try:
            json_db = json.load(f)
        except:
            json_db = {}
except:
    pass

bot = commands.Bot(command_prefix='!')

#variables needed for !uwu
#I mean what else would it be for?
json_db['uwu_suffixes'] = [
    ' ( ͡° ᴥ ͡°)',
    ' (´・ω・｀)',
    ' (ʘᗩʘ\')',
    ' (இωஇ )',
    ' (๑•́ ₃ •̀๑)',
    ' (• o •)',
    ' (⁎˃ᆺ˂)',
    ' (╯﹏╰）',
    ' (●´ω｀●)',
    ' (◠‿◠✿)',
    ' (✿ ♡‿♡)',
    ' (❁´◡`❁)',
    ' (　\'◟ \')',
    ' (人◕ω◕)',
    ' (；ω；)',
    ' (｀へ´)',
    ' ._.',
    ' :3',
    ' :D',
    ' :P',
    ' ;-;',
    ' ;3',
    ' ;_;',
    ' <{^v^}>',
    ' >_<',
    ' >_>',
    ' UwU',
    ' XDDD',
    ' ^-^',
    ' ^_^',
    ' x3',
    ' x3',
    ' xD',
    ' ÙωÙ',
    ' ʕʘ‿ʘʔ',
    ' ㅇㅅㅇ',
    ' （＾ｖ＾）'
]

json_db['uwu_substitutions'] = {
    'r': 'w',
    'l': 'w',
    'R': 'W',
    'L': 'W',
    'no': 'nyo',
    'No': 'Nyo',
    'has': 'haz',
    'have': 'haz',
    'you': 'uu',
    'the ': 'da ',
    'The ': 'Da ',
    'THE ': 'DA '
}

#Write to FS
with open(json_file, 'w') as f:
    json.dump(json_db, f)

# the following code is 100% stolen from @DerpyChap on GitHub with no shame
# https://github.com/DerpyChap/owotext/blob/master/owotext/owo.py
class OwO:
    # noinspection PyDefaultArgument
    def __init__(self, _suffixes=json_db['uwu_suffixes'], _substitutions=json_db['uwu_substitutions']):
        self.suffixes = _suffixes
        self.substitutions = _substitutions

    def whatsthis(self, text: str):
        """
        UwU Convewts da specified stwing into OwO speak ʕʘ‿ʘʔ
        :param text: Huohhhh. Da text uu want to convewt..
        :return: OWO Da convewted stwing (人◕ω◕)
        """
        text = self.translate(text)
        if self.suffixes:
            text = (text + " " + choice(self.suffixes))
        return text

    def translate(self, text: str):
        """
        Convewts da specified stwing into OwO speak, without a pwefix ow suffix
        :param text: Da text uu want to convewt
        :return: Da convewted stwing
        """
        for key, value in self.substitutions.items():
            text = text.replace(key, value)
        return text

o = OwO()

@bot.command()
async def ping(ctx):
    """
    Returns pong
    """
    await ctx.send('pong')

@bot.command()
async def whoisjoe(ctx):
    """
    Joe mama meme lolol
    """
    if "whoisjoe" in json_db:
        await ctx.send(json_db['whoisjoe'])
    else:
        await ctx.send("JOE MAMA")

@bot.command(hidden=True)
async def joeis(ctx, *, arg):
    """
    Will alter the output from whoisjoe
    """
    #Alter memory copy
    json_db['whoisjoe'] = arg
    #Write to FS
    with open(json_file, 'w') as f:
        json.dump(json_db, f)
    await ctx.message.delete()

@bot.command()
async def say(ctx, *, arg):
    """
    Says what you put
    """
    await ctx.send(arg)


@bot.command(hidden=True)
async def secret(ctx, *, arg=''):
    if(ctx.message.attachments):
        for a in ctx.message.attachments:
            await ctx.send(a.url)
    if(len(arg) > 0):
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
    """
    Adds the Role Messages
    """
    global messageDict
    global watched_message
    global emojiList
    for mess, emolist in messageDict.items():
        reacted_message = await ctx.send(mess)
        watched_message[reacted_message.id] = emolist
        f = open("dict.txt", "w")
        f.write(str(watched_message))
        f.close()
        for emo in emolist:
            await reacted_message.add_reaction(emo)


@bot.command()
async def myroles(ctx):
    """
    Lists roles of member that called this function
    """
    member = ctx.author
    s = ""
    iterroles = iter(member.roles)
    next(iterroles)
    for role in iterroles:
        s += role.name
        s += "\n"
    await ctx.send(f"Your roles:\n{s}")


@bot.command()
async def serverroles(ctx):
    """
    Lists roles of the server
    """
    s = ""
    roles = ctx.guild.roles
    iterroles = iter(roles)
    next(iterroles)
    for role in iterroles:
        if role.name == "hackbot 1.1":
            break
        else:
            s += role.name
            s += "\n"
    await ctx.send('Servers roles:\n%s' % s)


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
    """
    Tells you when you joined the server using UTC
    """
    member = ctx.author
    await ctx.send(
        f"Time {member.mention} joined {ctx.guild.name} in UTC:\n{member.joined_at}"
    )


@bot.command(pass_context=True)
async def roll(ctx, arg1="1", arg2="100"):
    """
    You can specify the amount of dice with a space or delimited with a 'd', else it will be 2 random nums between 1-6
    """
    await ctx.message.add_reaction('\U0001F3B2')
    author = ctx.message.author.mention  # use mention string to avoid pinging other people

    sum_dice = 0
    message = ""
    arg1 = str(arg1).lower()

    if ("d" in arg1):
        arg1, arg2 = arg1.split("d", 1)
        if (arg1 == ""):
            arg1 = "1"
        if (arg2 == ""):
            await ctx.send(f"Woah {author}, your rolls are too powerful")
            return

    if (not arg1.isdecimal() or not str(arg2).isdecimal()):
        await ctx.send(f"Woah {author}, your rolls are too powerful")
        return

    arg1 = int(arg1)
    arg2 = int(arg2)

    if (arg1 > 100 or arg2 > 100):
        await ctx.send(f"Woah {author}, your rolls are too powerful")
        return
    elif arg1 < 1 or arg2 < 1:
        await ctx.send(f"Woah {author}, your rolls are not powerful enough")
        return

    # Is it possible to be *too* pythonic?
    message += (
        f"{author} rolled {arg1} d{arg2}{(chr(39) + 's') if arg1 != 1 else ''}\n"
    )
    # Never.

    message += ("\n")
    for i in range(1, arg1 + 1):
        roll = randint(1, arg2)
        sum_dice += roll
        if (arg2 == 20 and roll == 20):
            message += (f"Roll {i}: {roll} - Critical Success! (20)\n")
        elif (arg2 == 20 and roll == 1):
            message += (f"Roll {i}: {roll} - Critical Failure! (1)\n")
        else:
            message += (f"Roll {i}: {roll}\n")

    message += ("\n")
    message += (f"Sum of all rolls: {sum_dice}\n")
    if (len(message) >= 2000):
        await ctx.send(f"Woah {author}, your rolls are too powerful")
    else:
        await ctx.send(message)

@bot.command(pass_context=True)
async def owo(ctx, arg1=""):
    """
    !owo Convewts da specified stwing into OwO speak ʕʘ‿ʘʔ

    uwusage: !owo Hello sir. Have you heard of our lord and savior Jesus Christ?
    returns: Hewwo siw. Have uu heawd of ouw wowd and saviow Jesus Chwist? (人◕ω◕)

    and uu can even input a message url ow message id!!!! (• o •)

    uwusage: !owo <message ID/message URL>
    returns: owofied message

    ow uu can simpwy use !owo by itsewf to owoify da pwevious message (╯﹏╰）

    uwusage: !owo
    returns: owofied message
    """
    await uwu(ctx, arg1)

@bot.command(pass_context=True)
async def uwu(ctx, arg1=""):
    """
    !uwu Convewts da specified stwing into OwO speak ʕʘ‿ʘʔ

    uwusage: !uwu Hello sir. Have you heard of our lord and savior Jesus Christ?
    returns: Hewwo siw. Have uu heawd of ouw wowd and saviow Jesus Chwist? (人◕ω◕)

    and uu can even input a message url ow message id!!!! (• o •)

    uwusage: !uwu <message ID/message URL>
    returns: uwufied message

    ow uu can simpwy use !uwu by itsewf to uwuify da pwevious message (╯﹏╰）

    uwusage: !uwu
    returns: uwufied message
    """
    await ctx.message.add_reaction('😽')
    argIsText = False
    channel = ctx.channel
    message = ""
    if(arg1 != ""):
        msg_id = arg1
        if(msg_id.isnumeric()):
            # arg1 is a direct message ID
            msg_id = int(arg1)
        elif(arg1.find('/') != -1):
            # arg1 is a link to a message
            msg_id = int(arg1.rsplit('/', 1)[1])
        else:
            argIsText = True

        if(not argIsText):
            message = await channel.fetch_message(msg_id)
            message = message.content
        else:
            # arg1 is original text that wants to be uwu-ized
            message = ctx.message.content.split(' ', 1)[1]
    else:
        # arg1 is nothing (grab the previous message)
        message = await channel.history(limit=2).flatten()
        message = message[1].content

    await ctx.send(o.whatsthis(message))

def get_server_uptime():
    """
    Helper function for uptime to get server uptime
    """
    result = subprocess.run(['uptime', '-p'], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").rstrip()

def pretty_print_uptime(time):
    #Chomp off the tiny bits
    time = int(time)
    #Need all data in terms of seconds
    minute = 60
    hour = minute * 60
    day = hour * 24
    days = time//day #How many days has this been up?
    time %= day #Get rid of days
    hours = time//hour
    time %= hour
    minutes = time//minute
    time %= minute
    seconds = time
    return f"up {days} days, {hours} hours, {minutes} minutes"

@bot.command()
async def uptime(ctx):
    """
    Displays the uptime of both the bot and the server the bot is running on
    """
    current = time.time()
    delta = current - start_time
    await ctx.send(f"Bot has been {pretty_print_uptime(delta)}\nServer has been {get_server_uptime()}")

@bot.command(hidden=True)
@commands.has_any_role('Cody', 'Dallas')
async def logout(ctx):
    """
    Logs the bot out
    """
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
    arr = [
        ''.join(
            [word[i] if i != 0 else word[i].upper() for i in range(len(word))])
        for word in arr
    ]
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
async def vaccines(ctx, loc="United States"):
    """
    Uses the information available at howmanyvaccinated.com to state how many people have been vaccinated based off location
    Will default to United States
    """
    url = "https://www.howmanyvaccinated.com/vaccine"
    page = requests.get(url)
    js = page.json()

    #Make sure that the location has every chance to succeed without fuzzy finding
    loc = normalize_location(loc)
    dat = gll(js, loc)
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
    rulesChannel = discord.utils.get(member.guild.channels,
                                     name='rules-and-info')
    await botChannel.send((
        f'Welcome to the server {member.mention}!\nPlease check out {rulesChannel.mention}!\nIn order to view channels you need to add the relevant roles.\
        Type !help for help, !serverroles for the roles you can add yourself to, !add "role1" "role2" to put yourself in that course.'
    ))


@bot.event
async def on_raw_reaction_add(payload):
    await manage_reactions(payload, True)


@bot.event
async def on_raw_reaction_remove(payload):
    await manage_reactions(payload, False)

#Role Commands for the bot

#Checks if the user has a role
def has_role(ctx, role):
    """
    Checks if the user previously had the role
    """
    member = ctx.author
    roles = [i.name for i in list(member.roles)]
    return role.name in roles

#Add roles for a user
@bot.command(pass_context=True)
async def add(ctx, *args):
    """
    Adds any roles mentioned after add if they exist say all for all roles possible to add
    One or many roles may be requested at a single time
    e.g. !add role1 role2 role3
    """
    r_success = []
    r_fail = []
    r_had = []
    member = ctx.author

    #Attempt to add users roles
    for arg in args:
        role = discord.utils.get(ctx.guild.roles, name=arg)
        try:
            #Check if user already had role
            if not has_role(ctx, role):
                await member.add_roles(role)
                r_success += [arg]
            else:
                r_had += [arg]
        except:
            r_fail += [arg]

    msg = ""
    if r_success:
        msg += f"I have succesfully added the role(s): {''.join(r_success)}\n"
    if r_had:
        msg += f"You were already in the role(s): {''.join(r_had)}\n"
    if r_fail:
        msg += f"I have failed to add the role(s): {''.join(r_fail)}\n"
    if r_fail:
        msg += "Please use !serverroles to check available roles and spelling\n"

    #Message back to user
    await ctx.send(f"{member.mention}:\n{msg}")

#Sub roles for a user
@bot.command(pass_context=True)
async def sub(ctx, *args):
    """
    Subtracts any roles mentioned after sub if they exist say all for all possible roles to remove
    One or many roles may be requested at a single time
    e.g. !sub role1 role2 role3
    """
    r_success = []
    r_fail = []
    r_had = []
    member = ctx.author
    for arg in args:
        role = discord.utils.get(ctx.guild.roles, name=arg)
        try:
            #Check if user didn't already have role
            if has_role(ctx, role):
                await member.remove_roles(role)
                r_success += [arg]
            else:
                r_had += [arg]
        except:
            r_fail += [arg]

    msg = ""
    if r_success:
        msg += f"I have succesfully removed the role(s): {''.join(r_success)}\n"
    if r_had:
        msg += f"You were not in the role(s): {''.join(r_had)}\n"
    if r_fail:
        msg += f"I have failed to remove the role(s): {''.join(r_fail)}\n"
    if r_had or r_fail:
        msg += "Please use !myroles to double check roles you are in and spelling\n"

    #Message back to user
    await ctx.send(f"{member.mention}:\n{msg}")

#bot.run(os.getenv('TOKEN'))
bot.run(token.stringToken())
