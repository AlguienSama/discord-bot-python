from discord.ext.commands import Context, Bot
from discord.utils import get
from discord import FFmpegPCMAudio, TextChannel
from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch

from utils.errors import CustomError
from .json_manage import get_queue, add_song, del_songs

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


async def join(bot: Bot, ctx: Context):
    try:
        channel = ctx.message.author.voice.channel
    except:
        raise CustomError('No estás conectado a ningún chat de voz')

    voice = get(bot.voice_clients, guild=ctx.guild)

    if not ctx.message.author.voice.channel:
        raise CustomError('No estás conectado a ningún chat de voz')

    if voice and voice.channel.id != ctx.message.author.voice.channel.id:
        raise CustomError('Ya está conectado a otro chat de voz')
    elif voice and voice.channel.id == ctx.message.author.voice.channel.id:
        pass
    else:
        voice = await channel.connect()
    return True


async def play(bot: Bot, ctx: Context, url: str):

    joined = await join(bot, ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)

    if url is not None:
        await add_queue(ctx, url)

    if joined:
        try:
            next_song(bot, ctx, False)
        except:
            pass

    else:
        await ctx.send("Bot is already playing")
        return


def next_song(bot, ctx, skip=True):
    if skip:
        del_queue(ctx, 1, 1)

    reproduce(bot, ctx)

    pass


async def skip(bot, ctx, first, last):
    if 0 < first < last:
        del_queue(ctx, first, last)
        return await ctx.send('Songs skiped')
    elif first > 0 and last <= first:
        del_queue(ctx, first, first)
    else:
        del_queue(ctx, 1, 1)

    if first == 1 or first == 0:
        next_song(bot, ctx, False)
    
    await ctx.send('Song skiped')


async def queue(ctx):
    try:
        queue = await get_queue(ctx.guild.id)
    except:
        raise CustomError('Empty Queue')

    text = f'```autohotkey\nQUEUE FOR {ctx.guild.name}\n'
    for i, s in enumerate(queue):
        text += f'#{i+1} : {s["name"]}\n'
    text += '```'
    await ctx.send(text)


async def add_queue(ctx, song):
    queue = add_song(ctx.guild.id, ctx.author.id, 'name', song)
    await ctx.send('Added to queue')


def del_queue(ctx, first, last):
    print('DEL QUEUE LAST')
    print(last)
    if last == 0:
        last = first
    
    del_songs(ctx.guild.id, first, last)


def reproduce(bot, ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    song = get_queue(ctx.guild.id)
    print(song)
    if song == []:
        print('finished')
        return
    song = song[0]
    print('SONGS')
    print(song)

    if voice.is_playing():
        print('is playing')
        voice.stop()
    else:
        print('not playing')

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(song['url'], download=False)
    TITLE = info['title']
    URL = info['url']
    try:
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: next_song(bot, ctx))
    except:
        pass
    voice.is_playing()

    return TITLE


def parse_duration(duration: int):
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    duration = []
    if days > 0:
        duration.append('{} días'.format(days))
    if hours > 0:
        duration.append('{} horas'.format(hours))
    if minutes > 0:
        duration.append('{} minutos'.format(minutes))
    if seconds > 0:
        duration.append('{} segundos'.format(seconds))

    return ', '.join(duration)
