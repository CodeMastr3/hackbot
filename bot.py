import discord
import discord.utils
#import emojiRole.py
import token1

from discord.ext import commands

bot = commands.Bot(command_prefix='!')

"""watched_messages = {
    messageID: {
        regularEmojiName: roleID,
        customEmojiID: roleID
    }
}
"""
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def addMessage(ctx):
    global watched_message
    global emojiList
    reacted_message = await ctx.send("Hi")
    print(reacted_message)
    emoji = '\N{THUMBS UP SIGN}'
    emojiList[emoji] = '685902355404947535'
    watched_message[reacted_message.id] = emojiList
    await reacted_message.add_reaction(emoji)

@bot.command()
async def logout(ctx):
    await bot.logout()

watched_message = {}
emojiList = {}
emojiList1 = {}

emojiList1['afc96e77efee1190e1fbe3cc69f149f8'] = '<@&685902355404947535>'
emojiList1['df854ca9a022bf3b5fe42ded8725e1bc'] = '<@&685891891006275604>'

watched_message['22'] = emojiList1

async def manage_reactions(ctx, reaction, user, added: bool):
    print("I'm in")
    global watched_message
    if not reaction.message.id in watched_message:
        print("I'm not supposed to be out????")
        return

    print("I got here")
    messageID = reaction.message.id
    mapping = watched_message[messageID]
    if not reaction.emoji in mapping:
        # reaction.emoji is str if normal emoji or ID if custom, but we use both as keys in mapping
        return

    print("I got even farther")
    #member = discord.utils.get(reaction.message.guild.members, id=user.id)
    print(user)
    #print(member)
    role = discord.utils.get(reaction.message.guild.roles, id=mapping[reaction.emoji])
    role1 = RoleConverter.convert(ctx, '685902355404947535')

    if added:
        await user.add_roles(role1)
    else:
        await user.remove_roles(role)

@bot.event
async def on_reaction_add(ctx, reaction, user):
    print("About to go into manage_reactions for add")
    await manage_reactions(reaction, user, added=True)

@bot.event
async def on_reaction_remove(ctx, reaction, user):
    await manage_reactions(reaction, user, added=False)

































bot.run(token1.stringToken())
