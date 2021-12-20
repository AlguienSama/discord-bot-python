from utils.together import DiscordTogether
from utils.responses.Embed import Embed
from discord.ext.commands import VoiceChannelConverter
from discord import VoiceChannel
from utils.errors import CustomError


async def youtube_together(ctx, channel):
    return await discord_together(ctx, channel, 'youtube')


async def poker_together(ctx, channel):
    await discord_together(ctx, channel, 'poker')


async def betrayal_together(ctx, channel):
    await discord_together(ctx, channel, 'betrayal')


async def fishing_together(ctx, channel):
    await discord_together(ctx, channel, 'fishing')


async def chess_together(ctx, channel):
    await discord_together(ctx, channel, 'chess')


async def discord_together(ctx, channel, type):
    channel: VoiceChannel = await VoiceChannelConverter().convert(ctx, channel)

    embed = Embed().success()

    if type == 'youtube':
        embed.title = '!! Youtube Together !!'
    elif type == 'poker':
        embed.title = '!! Poker Together !!'
    elif type == 'betrayal':
        embed.title = '!! Betrayal Together !!'
    elif type == 'fishing':
        embed.title = '!! Fishing Together !!'
    elif type == 'chess':
        embed.title = '!! Ajedrez !!'
    else:
        raise CustomError('Nope')

    url: DiscordTogether = await DiscordTogether().create_together_code(channel.id, type)

    embed.description = f'Pulsa [aquí]({url}) para entrar!'

    await ctx.send(embed=embed.get_embed())
