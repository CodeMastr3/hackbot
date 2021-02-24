import discord
from discord.ext import commands
from random import randint

#client = commands.Bot(command_prefix = "!")

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """
        Returns pong
        """
        await ctx.send('pong')

    @commands.command()
    async def say(self, ctx, *, arg):
        """
        Says what you put
        """
        await ctx.send(arg)

    @commands.command(hidden=True)
    async def secret(self, ctx, *, arg=''):
        if(ctx.message.attachments):
            for a in ctx.message.attachments:
                await ctx.send(a.url)
        if(len(arg) > 0):
            await ctx.send(arg)
        await ctx.message.delete()

    @commands.command()
    async def escalate(self, ctx):
        await ctx.send('ESCALATING')

    @commands.command(pass_context=True)
    async def roll(self, ctx, arg1="1", arg2="100"):
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

    #@client.event
    @commands.command(pass_context=True)
    async def ban(self, ctx, arg1=""):
        """
        Bans (but not actually) the person specified in the first argument.
        If argument is an empty string, assume it was the last person talking
        """

        message = ""

        # Courtesy of https://stackoverflow.com/questions/61243162/discord-py-how-to-detect-if-a-user-mentions-pings-the-bot
        #bot_name = client.user.mention

        if arg1 != "":
            #if bot_name not in arg1:
            message = "brb, banning " + arg1
            #elif bot_name in arg1:
            #    message = ctx.message.author.mention + " you can't ban me!"
        else:
            channel = ctx.channel
            prev_author = await channel.history(limit=2).flatten()
            prev_author = prev_author[1].author.mention
            
            #if prev_author != bot_name:
            message = "brb, banning " + prev_author
            #else:
            #    message = ctx.message.author.mention + " you can't ban me!"
            
        await ctx.send(message)
            

def setup(bot):
    bot.add_cog(FunCog(bot))
