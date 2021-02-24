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

#Write to FS
with open(json_file, 'w') as f:
    json.dump(json_db, f)


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
