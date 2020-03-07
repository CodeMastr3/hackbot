import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('Njg1ODg4MjEzOTI3MTk4OTU3.XmPNaw.hoUzeROSUpW9YxvHYx1wnZYoaF8')

