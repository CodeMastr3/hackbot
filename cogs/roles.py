import ast
import discord
import sys
sys.path.append("..")
from emojiRole import message as emojiRolemessage
from discord.ext import commands

#Role Commands for the bot

messageDict = emojiRolemessage
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
class RolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role('Cody', 'Dallas')
    async def addMessage(self, ctx):
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

    @commands.command(name='myroles', aliases=['myr', 'mr'])
    async def myroles(self, ctx):
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
        await ctx.reply(f"Your roles:\n{s}")

    @commands.command(name='serverroles', aliases=['sr'])
    async def serverroles(self, ctx):
        """
        Lists the roles that this bot can add you to
        To add any role(s) to yourself, please view !add and !del
        """
        roles = self.bot_roles(ctx, ignore_preamble=False)
        bs = "\n" #bs stands for "Backslash" but it's bs i can't do a \n in {} for f-strings
        await ctx.send(f"Server's Roles:{bs}{bs}{bs.join([i.name for i in roles])}")

    async def manage_reactions(self, payload, added: bool):
        if not payload.message_id in watched_message:
            return

        messageID = payload.message_id
        mapping = watched_message[messageID]

        if not payload.emoji.name in mapping:
            # reaction.emoji is str if normal emoji or ID if custom, but we use both as keys in mapping
            return

        guildName = self.bot.get_guild(payload.guild_id)
        member = discord.utils.get(guildName.members, id=payload.user_id)
        role = discord.utils.get(guildName.roles, name=mapping[payload.emoji.name])

        if added:
            await member.add_roles(role)
        else:
            await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.manage_reactions(payload, True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        await self.manage_reactions(payload, False)

    #Checks if the user has a role
    def has_role(self, ctx, role):
        """
        Checks if the user previously had the role
        """
        member = ctx.author
        roles = [i.name for i in list(member.roles)]
        return role.name in roles

    #Gets all the roles the bot can configure
    def bot_roles(self, ctx, ignore_preamble=True):
        validRoles = []
        roles = ctx.guild.roles[1:] #Strip @everyone
        stopRole = self.bot.user.name #Everything below bot's name's role is ommitted
        for role in roles:
            if role.name == stopRole:
                break
            if not ignore_preamble or not role.name.startswith("|---"): #Preamble for organization
                validRoles += [role]
        return validRoles[::-1]

    #Add roles for a user
    @commands.command(pass_context=True)
    async def add(self, ctx, *args):
        """
        Adds any roles mentioned after add if they exist say all for all roles possible to add
        One or many roles may be requested at a single time
        e.g. !add role1 role2 role3
        """
        r_success = []
        r_fail = []
        r_had = []
        member = ctx.author
        br = self.bot_roles(ctx)

        if "all" in args:
            for role in br:
                if not self.has_role(ctx, role):
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
                        if not self.has_role(ctx, role):
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
        await ctx.reply(f"{msg}")

    #Remove roles for a user
    @commands.command(pass_context=True, name="del", aliases=['rm'])
    async def sub(self, ctx, *args):
        """
        Subtracts any roles mentioned after del if they exist say all for all possible roles to remove
        One or many roles may be requested at a single time
        e.g. !del role1 role2 role3
        """
        r_success = []
        r_fail = []
        r_had = []
        member = ctx.author
        br = self.bot_roles(ctx)
        if "all" in args:
            for role in br:
                if self.has_role(ctx, role):
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
                        if self.has_role(ctx, role):
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
        await ctx.reply(f"{msg}")

    @commands.command(pass_context=True, name="private")
    async def private(self, ctx, *args):
        """
        Removes a message that the bot had sent
        """
        member = ctx.author
        author = self.bot.user
        channel = ctx.channel
        message = ctx.message
        if len(args) >= 2:
            for arg in args:
                deletion = await channel.fetch_message(arg)
                mentioned = deletion.mentions
                if member in mentioned and deletion.author == author:
                    await discord.Message.delete(deletion)
                else:
                    sent = await ctx.reply("You can't delete that message")
                    await sent.delete(delay=5)
                await message.delete(delay=5)
        elif message.reference is not None:
            deletion = await channel.fetch_message(message.reference.resolved.id)
            if member in deletion.mentions and deletion.author == author:
                await discord.Message.delete(deletion)
            else:
                sent = await ctx.reply("You can't delete that message")
                await sent.delete(delay=5)
            await message.delete(delay=5)
        else:
            deletion = await channel.history(limit=2).flatten()
            if member in deletion[1].mentions and deletion[1].author == author:
                await discord.Message.delete(deletion[1])
            else:
                sent = await ctx.reply("You can't delete that message")
                await sent.delete(delay=5)
            await message.delete(delay=5)

def setup(bot):
    bot.add_cog(RolesCog(bot))
