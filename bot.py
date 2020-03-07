import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def logout(ctx):
    await bot.logout()





























bot.run('Njg1ODkyNjI2NzI5MjcxMzk1.XmPRTw.dkOEenS7SnJK-isZBTtpM0Ny-zE')

