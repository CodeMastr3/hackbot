import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

watched_messages = {
    messageID: {
        regularEmojiName: roleID,
        customEmojiID: roleID
    }
}

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def addMessage(ctx):
    reacted_message = await client.send("Hi")
    reacted_message.add_reaction(emoji)

@bot.command()
async def logout(ctx):
    await bot.logout()

async def manage_reaction(self, reaction, user, added: bool):
    if not reaction.message.id in self.watched_messages:
        return

    messageID = reaction.message.id
    mapping = self.watched_messages[messageID]
    if not reaction.emoji in mapping:
        return

    member = discord.utils.get(reaction.message.server.members, id=user.id)
    role = discord.utils.get(reaction.message.server.roles, id=mapping[reaction.emoji])

    if added:
        await bot.add_roles(member, role)
    else:
        await bot.remove_roles(member, role)

@bot.event
async def on_reaction_add(self, reaction, user):
    await self.manage_reactions(reaction, user, True)

@bot.event
async def on_reaction_remove(self, reaction, user):
    await self.manage_reactions(reaction, user, False)

bot.run('Njg1ODkyNjI2NzI5MjcxMzk1.XmPRTw.dkOEenS7SnJK-isZBTtpM0Ny-zE')
