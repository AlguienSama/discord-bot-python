import discord
from discord.ext import commands

from commands.games.commands.tic_tac_toe import tic_tac_toe

bot = commands.Bot(command_prefix='*', description='pito', owner=355104003572498435,case_insensitive=True)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle)
    # with open('unknown.png', 'rb') as f:
    #    await bot.user.edit(avatar=f.read())
    print('Logged in as @' + bot.user.name + '#' + bot.user.discriminator)


@bot.event
async def on_message(message):
    async for message in message.channel.history(limit=1):
        print(message.content)
    if message.author.id == 795726334995202051:
        return

    if '3raya' in message.content:
        await tic_tac_toe(bot, message)


bot.run('Nzk1NzI2MzM0OTk1MjAyMDUx.YjUCHQ.cE9aljG6A21oQUW9itrqI-cpq4I', bot=False)