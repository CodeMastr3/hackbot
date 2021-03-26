import discord
from discord.ext import commands
from random import randint, choice



class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_user_self(self, user_mentioned):
        bot_as_user = self.bot.user
        if (user_mentioned.name == bot_as_user.name 
        and user_mentioned.discriminator == bot_as_user.discriminator
        and user_mentioned.bot):
            return True
        else:
            return False

    def make_ban_message(self, user_mentioned):
        ban_messages = [
            f"brb, banning {user_mentioned}.",
            f"you got it, banning {user_mentioned}.",
            f"{user_mentioned}, you must pay for your crimes. A ban shall suffice.",
            f"today's controvesial opinion reward goes to {user_mentioned}. The prize? A ban, duh.",
            f"{user_mentioned} gotta ban you now. Sorry.",
            f"{user_mentioned} stop talking before you--oh, wait. Too late.",
        ]
        ban_easter_eggs = [
            f"{user_mentioned} I WARNED YOU ABOUT STAIRS BRO. I TOLD YOU.",
            f"Let's be honest with ourselves: we just wanted to ping {user_mentioned} twice.",
            f"{user_mentioned} has broken the unspoken rule.",
        ]
        odds = randint(1, 1000)
        if odds > 900:
            return choice(ban_easter_eggs)
        return choice(ban_messages)

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

    @commands.command(pass_context=True)
    async def ban(self, ctx):
        """
        Bans (but not actually) the person mentioned.
        If argument is an empty string, assume it was the last person talking.
        """
        cannot_ban_bot = ctx.message.author.mention + " you can't ban me!"
        user_attempted_bot_ban = False

        mentions_list = ctx.message.mentions
        message_text = ctx.message.content

        ban_has_text = False
        if len(mentions_list) < 1 \
        and len(message_text.split(" ")) > 1:
            ban_has_text = True

        message = ""
        user_mentioned = ""

        # Check that only one user is mentioned
        if len(mentions_list) > 1:
            # Multiple user ban not allowed
            await ctx.send(ctx.message.author.mention + " woah bucko, one ban at a time, please!")
        elif len(mentions_list) == 1:
            # One user ban at a time.
            # If the user not a bot, ban them. Otherwise, special message.
            user_mentioned = mentions_list[0]
            if not self.is_user_self(user_mentioned):
                # Check that the user being banned is not a professor.
                # Get user's roles
                roles_raw = ctx.message.guild.get_member(user_mentioned.id).roles
                roles = []
                # Turn into list, and lowercase it.
                for role in roles_raw:
                    roles.append(role.name)
                roles_lower = [i.lower() for i in roles]
                # Tell users who try to ban a professor that they may not do so.
                if "professors" in roles_lower:
                    message = ctx.message.author.mention + " you can't ban a professor."
                else:
                    message = self.make_ban_message(user_mentioned.mention)
            else:
                user_attempted_bot_ban = True
                message = cannot_ban_bot
        else:
            if ban_has_text:
                # Some users apparently want to "!ban me", "!ban you", or other edge cases.
                # This is where we handle that.
                message_text = ctx.message.content[5:]
                if message_text == "me":
                    # Person executing the command wants to be banned.
                    user_mentioned = ctx.message.author.mention
                    message = self.make_ban_message(ctx.message.author.mention)
                elif message_text == "you":
                    channel = ctx.channel
                    prev_author = await channel.history(limit=2).flatten()
                    user_being_banned = prev_author[1].author
                    prev_author = prev_author[1].author.mention
                    user_mentioned = prev_author

                    if not self.is_user_self(user_being_banned):
                        message = self.make_ban_message(prev_author)
                    else:
                        user_attempted_bot_ban = True
                        message = cannot_ban_bot
                else:
                    # I guess we're just banning whatever now, then ¯\_(ツ)_/¯
                    if message_text == "charon":
                        # Unless it's the bot 🙅‍♂️
                        user_attempted_bot_ban = True
                        message = cannot_ban_bot
                    else:
                        message = self.make_ban_message(message_text)
            else:
                channel = ctx.channel
                prev_author = await channel.history(limit=2).flatten()
                user_being_banned = prev_author[1].author
                prev_author = prev_author[1].author.mention
                
                if not self.is_user_self(user_being_banned):
                    message = self.make_ban_message(prev_author)
                else:
                    user_attempted_bot_ban = True
                    message = cannot_ban_bot

        odds = randint(1, 100)
        if odds > 99 and not user_attempted_bot_ban:
            # 1 in 100 chance of getting a gif instead.
            if user_mentioned != "":
                await ctx.send(user_mentioned)
                await ctx.send("https://c.tenor.com/d0VNnBZkSUkAAAAM/bongocat-banhammer.gif")
                return
            else:
                await ctx.send(message_text)
                await ctx.send("https://c.tenor.com/d0VNnBZkSUkAAAAM/bongocat-banhammer.gif")
                return
        await ctx.send(message)

# Adds the cog to the bot
def setup(bot):
    bot.add_cog(FunCog(bot))
