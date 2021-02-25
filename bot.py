import discord
import discord.utils
import emojiRole
import token1 as token
import ast
import requests
import subprocess
import os
import json
import re

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

announcementChanName = "Announcement"

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

# Bot Setup -- Attempt to set up greeting. If it fails, then go without it
intents = discord.Intents(messages=True, guilds=True)
try:
    intents.members = True
    bot = commands.Bot(command_prefix='!', intents=intents)
except:
    bot = commands.Bot(command_prefix='!', intents=intents)

#variables needed for !uwu
#I mean what else would it be for?
json_db['uwu_suffixes'] = [
    ' (´・ω・｀)',
    ' (๑•́ ₃ •̀๑)',
    ' (• o •)',
    ' (⁎˃ᆺ˂)',
    ' (╯﹏╰）',
    ' (●´ω｀●)',
    ' (◠‿◠✿)',
    ' (✿ ♡‿♡)',
    ' (❁´◡\`❁)',
    ' (　\'◟ \')',
    ' (；ω；)',
    ' (´･ω･\`)',
    ' o3o',
    ' :3',
    ' :D',
    ' :P',
    ' ;\_;',
    ' <{^v^}>',
    ' >\_<',
    ' UwU',
    ' ^-^',
    ' xD',
    ' ÙωÙ',
    ' ㅇㅅㅇ',
    ' （＾ｖ＾）',
    ' \*starts howling\*',
    ' \*leaps up and down\*',
    ' \*wags tail\*',
]

json_db['uwu_substitutions'] = {
    'r': 'w',
    'l': 'w',
    'the ': 'da ',
    'th': 'd',
    'hi': 'hai',
    'has': 'haz',
    'have': 'haz',
    'is': 'iws',

    # some words have already been uwu-ized
    'fuck' : 'henck',
    'bitch' : 'vewwy nice lady',
    'shait' : 'poot',
    ' ass ' : ' fwuffey tail ',
    'kill' : 'nuzzle',
    'god' : 'sonic',
    'jesus christ' : 'cheese and wice',
    'degenewates' : 'cutie pies',
    'degenewate' : 'cutie pie',
    'diwsgusting' : 'bulgy wulgy',
    'gwossest' : 'bulgiest',
    'gwoss' : 'AMAZEBALLS (✿ ♡‿♡)',
    'nasty' : 'musky',
    'hand' : 'paw',

    # compounding uwu-ness
    'uwu' : 'uwuwuwu',
    'owo' : 'owowowo',
    'you ' : 'uwu ',
    'dude': 'duwude',
    'to' : 'towo',
    'no' : 'nowo',
    'oh' : 'owo',
    'do ' : 'dowo ',
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

        text = re.sub(r'<a?:\S+:[0-9]+>\s?', '', text) # remove private server emojis
        for key, value in self.substitutions.items():
            text = text.replace(key, value)
        i = 0
        while i < len(text):
            # occasionally convert end of sentance punctuation into a uwu suffix
            if(text[i] == '.' or text[i] == '?' or text[i] == '!'):
                if(randint(0, 5) == 0):
                    seed(i) # random is not very random apparently
                    randSuffix = self.suffixes[randint(0, len(self.suffixes)-1)]
                    text = text[:i] + randSuffix + text[i + 1:]
            i += 1

        return text

o = OwO()

@bot.command()
async def ping(ctx):
    """
    Returns pong
    """
    await ctx.send('pong')

# detect stock tickers and display their current price
@bot.listen('on_message')
async def on_message(message):
    msg_str = await message.channel.fetch_message(message.id)
    msg_str = msg_str.content

    output_msg = ""

    # ignore user commands, as well as responses by the bot
    if(msg_str[0] == "!" or message.author.bot):
        return

    matches = re.finditer("\$[a-zA-Z]+", msg_str)
    num_matches = 0
    for match in matches:
        stock = msg_str[match.start()+1:match.end()]
        # token is publishable
        request_url = f"https://cloud.iexapis.com/stable/stock/{stock}/quote?token=pk_b2df4f042df34774b50c5693366f8a57"

        page = requests.get(request_url)
        if(page.status_code != 200):
            continue

        num_matches += 1
        js = page.json()

        output_msg += f"➝ {stock.upper()} ({js['companyName']}) - "
        if('isUSMarketOpen' in js and not js['isUSMarketOpen']):
          output_msg += f"Current price: ${str(js['latestPrice'])}\n"
          output_msg += f"\t\tAfter hours price: **${str(js['extendedPrice'])}**\n"
        else:
          output_msg += f"Current price: **${str(js['latestPrice'])}**\n"

    if(num_matches == 0):
      return

    # we are not guarenteed to respond until at least this line
    await message.add_reaction('📈')

    output_msg = "I have detected " + str(num_matches) + f" stock ticker{('s') if num_matches != 1 else ''} in your message\n\n" + output_msg
    output_msg += "\n"
    output_msg += "ᴡᴇ ᴅᴏ ɴᴏᴛ ɢᴜᴀʀᴀɴᴛᴇᴇ ᴛʜᴇ ᴀᴄᴄᴜʀᴀᴄʏ ᴏғ ᴛʜɪs ᴅᴀᴛᴀ"
    channel = await discord.Client.fetch_channel(bot, message.channel.id)
    await channel.send(output_msg)

@bot.command()
async def whoisjoe(ctx):
    """
    Joe mama meme lolol
    """
    if "whoisjoe" in json_db:
        await ctx.send(json_db['whoisjoe'])
    else:
        await ctx.send("JOE MAMA")

@bot.command()
async def prse(ctx):
    """
    because of course we need a !prse command
    """
    await ctx.send("PReSEnting: https://github.com/Asterisk007/prse\n[This programming language is not endorsed by the University, nor this Discord server.]")

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
    Lists the roles that this bot can add you to
    To add any role(s) to yourself, please view !add and !sub
    """
    roles = bot_roles(ctx, ignore_preamble=False)
    bs = "\n" #bs stands for "Backslash" but it's bs i can't do a \n in {} for f-strings
    await ctx.send(f"Server's Roles:{bs}{bs}{bs.join([i.name for i in roles])}")


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
    You can specify the amount of dice with a space or delimited with a 'd', 
    else it will be 2 random nums between 1-6
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
            # arg1 is a message ID
            msg_id = int(arg1)
        elif(arg1.find('-') != -1):
            text = arg1.rsplit('-', 1)[1]
            if(text.isnumeric()):
                # arg1 is a message ID in the form of <channelID>-<messageID>
                msg_id = int(text)
            else:
                argIsText = True
        elif(arg1.find('/') != -1):
            text = arg1.rsplit('/', 1)[1]
            if(text.isnumeric()):
                # arg1 is a link to a message
                msg_id = int(text)
            else:
                argIsText = True
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

    message = o.whatsthis(message.lower())
    if(len(message) > 2000):
      message = "OWO youw message is too bulgy wulgy fow me to send"
    await ctx.send(message)

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
    await ctx.send(f"Bot has been {pretty_print_uptime(delta)}\nServer has \
    been {get_server_uptime()}")

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
    Will change a phrase like "uNITED sTATES" to "United States" since all 
    location are stored as proper nouns
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

def sll(js, loc):
    """
    Used for the vaccines command, will search through and try to find the state's
    information using newegg's data
    Heck newegg
    """
    loc = loc.lower()
    for s in js:
        if s['Location'].lower() == loc or s['ShortName'].lower() == loc or s['LongName'].lower() == loc:
            return s
    return None


@bot.command()
async def vaccines(ctx, loc="United States"):
    """
    Uses the information available at howmanyvaccinated.com to state how many
    people have been vaccinated based off location
    Will default to United States
    """
    url = "https://www.howmanyvaccinated.com/vaccine"
    states_url = "https://promotions.newegg.com/EC/covid19/vaccination/vaccina.json"

    page = requests.get(url)
    states_page = requests.get(states_url)
    js = page.json()
    states_js = states_page.json()

    state_dat = sll(states_js["vaccination_data"], loc)
    dat = None
    if state_dat is None: #Should only do extra work if can't find state data
        dat = gll(js, normalize_location(loc))

    msg = ""
    if state_dat is not None:
        ad1 = "{:,}".format(int(state_dat['Administered_Dose1']))
        ad2 = "{:,}".format(int(state_dat['Administered_Dose2']))

        msg = (f"In {state_dat['LongName']} as of {state_dat['Date']}, there have been "
               f"{ad1}({state_dat['Administered_Dose1_Pop_Pct']}%) "
               f"persons who have received Dose 1, "
               f"{ad2}({state_dat['Administered_Dose2_Pop_Pct']}%) persons who have received Dose 2")

    elif dat is not None:
        #Format the number with commas to make it easier to read
        tot = "{:,}".format(int(dat['total_vaccinations']))
        msg = f"In {loc} as of {dat['date']}, there have been {tot}\
         vaccinations, totalling {dat['total_vaccinations_per_hundred']}% of\
         the population."
        msg = ' '.join(msg.split())
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
    rulesChannel = discord.utils.get(member.guild.channels, name='rules-and-info')
    try:
        role = discord.utils.get(member.guild.roles, name=announcementChanName)
        await member.add_roles(role)
    except:
        pass
    msg1 = f"Welcome to the server {member.mention}!"
    msg2 = f"Please check out {rulesChannel.mention}!"
    msg3 = "In order to view channels you need to add the relevant roles."
    msg4 = "Type `!help` for help, `!serverroles` for the roles you can add \
        yourself to, `!add role1 role2` to put yourself in that course."
    msg4 = " ".join(msg4.split())
    msg5 = f"You have already been added to the \
        {announcementChanName} role, so that you can keep up to date on any events\
         that might be happening and things you might want to be aware of. \
         Feel free to remove yourself from this role by saying `!sub \
         {announcementChanName}` in {botChannel.mention}"
    msg5 = " ".join(msg5.split())
    msgList = [msg1, msg2, msg3, msg4, msg5]
    msg = "\n".join(msgList)
    await botChannel.send(msg)


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

#Gets all the roles the bot can configure
def bot_roles(ctx, ignore_preamble=True):
    validRoles = []
    roles = ctx.guild.roles[1:] #Strip @everyone
    stopRole = bot.user.name #Everything below bot's name's role is ommitted
    for role in roles:
        if role.name == stopRole:
            break
        if not ignore_preamble or not role.name.startswith("|---"): #Preamble for organization
            validRoles += [role]
    return validRoles[::-1]

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
    br = bot_roles(ctx)

    if "all" in args:
        for role in br:
            if not has_role(ctx, role):
                try:
                    await member.add_roles(role)
                    r_success += [role.name]
                except:
                    pass #Don't care about extraneous roles
    else:
        #Attempt to add users roles
        for arg in args:
            role = discord.utils.get(ctx.guild.roles, name=arg)
            if role not in br: #Check if it's an accepted role first
                r_fail += [arg]

            else:
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
        msg += f"I have succesfully added the role(s): {' '.join(r_success)}\n"
    if r_had:
        msg += f"You were already in the role(s): {' '.join(r_had)}\n"
    if r_fail:
        msg += f"I have failed to add the role(s): {' '.join(r_fail)}\n"
    if r_fail:
        msg += "Please use !serverroles to check available roles and spelling\n"

    if not msg:
        msg = "I did nothing"

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
    br = bot_roles(ctx)
    if "all" in args:
        for role in br:
            if has_role(ctx, role):
                try:
                    await member.remove_roles(role)
                    r_success += [role.name]
                except:
                    pass #Don't care about extraneous roles
    else:
        for arg in args:
            role = discord.utils.get(ctx.guild.roles, name=arg)
            if role not in br: #Check if it's an accepted role first
                r_fail += [arg]

            else:
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
        msg += f"I have succesfully removed the role(s): {' '.join(r_success)}\n"
    if r_had:
        msg += f"You were not in the role(s): {' '.join(r_had)}\n"
    if r_fail:
        msg += f"I have failed to remove the role(s): {' '.join(r_fail)}\n"
    if r_had or r_fail:
        msg += "Please use !myroles to double check roles you are in and spelling\n"

    if not msg:
        msg = "I did nothing"

    #Message back to user
    await ctx.send(f"{member.mention}:\n{msg}")

@bot.command()
@commands.has_any_role('Cody', 'Dallas')
async def update(ctx):
    update_script = "./update.sh"
    if os.path.exists(update_script):
        await ctx.send("Attempting to Update")
        subprocess.run(["./update.sh"])
    else:
        await ctx.send("Update Script Not Found")

#bot.run(os.getenv('TOKEN'))
bot.run(token.stringToken())
