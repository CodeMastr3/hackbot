import discord
import discord.utils
import ast
import os
import json
import re
import subprocess

from dotenv import load_dotenv
from random import seed
from random import randint
from random import choice
from discord.ext import commands

load_dotenv('.env')
json_file = "db.json"
json_db = {}
try:
    with open(json_file, 'r') as f:
        try:
            json_db = json.load(f)
        except:
            json_db = {}
except:
    pass

announcementChanName = "Announcement"

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
            if "uwu-immune" in [r.name.lower() for r in message.author.roles]:
                await ctx.send("UwU this usew is uwu-immune! sowwy... 😭")
                return
            else:
                message = message.content
        else:
            # arg1 is original text that wants to be uwu-ized
            if "uwu-immune" in [r.name.lower() for r in ctx.message.author.roles]:
                await ctx.send("UwU you'we immune to the uwu! sowwy... 😭")
                return
            else:
                message = ctx.message.content.split(' ', 1)[1]
    else:
        # arg1 is nothing (grab the previous message)
        message = await channel.history(limit=2).flatten()
        if "uwu-immune" in [r.name.lower() for r in message[1].author.roles]:
            await ctx.send("UwU this usew is uwu-immune! sowwy... 😭")
            return
        else:
            message = message[1].content

    message = o.whatsthis(message.lower())
    if(len(message) > 2000):
      message = "OWO youw message is too bulgy wulgy fow me to send"
    await ctx.send(message)

@bot.command(hidden=True)
@commands.has_any_role('Cody', 'Dallas')
async def logout(ctx):
    """
    Logs the bot out
    """
    await bot.logout()

@logout.error
async def logout_error(ctx, error):
    await ctx.channel.send("You don't have the permission to run that command")

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

@bot.command()
@commands.has_any_role('Cody', 'Dallas')
async def update(ctx):
    update_script = "./update.sh"
    if os.path.exists(update_script):
        await ctx.send("Attempting to Update")
        subprocess.run(["./update.sh"])
    else:
        await ctx.send("Update Script Not Found")

initial_extensions = ['cogs.roles', 'cogs.info', 'cogs.fun']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(os.getenv('TOKEN'))
