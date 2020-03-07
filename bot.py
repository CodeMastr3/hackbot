import discord
#import emojiRole.py
import token1

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

watched_message = {}
emojiList1 = {}

emojiList1['afc96e77efee1190e1fbe3cc69f149f8'] = '<@&685902355404947535>'
emojiList1['df854ca9a022bf3b5fe42ded8725e1bc'] = '<@&685891891006275604>'

watched_message['22'] = emojiList1

async def manage_reaction(self, reaction, user, added: bool):
    if not reaction.message.id in self.watched_messages:
        return

    messageID = reaction.message.id
    mapping = self.watched_messages[messageID]
    if not reaction.emoji in mapping:
        # reaction.emoji is str if normal emoji or ID if custom, but we use both as keys in mapping
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

bot.run(token1.stringToken())
