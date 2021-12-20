from discord import User, Member
from discord.ext.commands import Context, MemberConverter, UserConverter
from utils.errors import CustomError
from utils.responses.Embed import Embed
from utils.ddbb.user_moderation import *


async def warn(ctx: Context, user, *, reason: str):
    try:
        id = await set_warn(ctx.guild, user, ctx.author, reason)
        await _send_message(ctx, user, ctx.author, id, 'warn')
    except Exception as e:
        print(e)

    pass


async def mute(ctx: Context, user: User, *, reason: str):
    try:
        id = await set_mute(ctx.guild, user, ctx.author, reason)
        await _send_message(ctx, user, ctx.author, id, 'mute')
    except Exception as e:
        print(e)

    pass


async def kick(ctx: Context, user: User, *, reason: str = ''):
    try:
        await ctx.guild.kick(user=user, reason=reason)
        id = await set_kick(ctx.guild, user, ctx.author, reason)
        await _send_message(ctx, user, ctx.author, id, 'kick')
    except Exception as e:
        print(e)
        CustomError('Error al kickear')

    pass


async def ban(ctx: Context, user: User, *, reason: str):
    try:
        await ctx.guild.ban(user=user, reason=reason)
        id = await set_ban(ctx.guild, user, ctx.author, reason)
        await _send_message(ctx, user, ctx.author, id, 'ban')
    except Exception as e:
        print(e)
        CustomError('Error al bannear')

    pass


async def unban(ctx: Context, user: User, *, reason: str):
    try:
        await ctx.guild.unban(user=user, reason=reason)
        id = await set_unban(ctx.guild, user, ctx.author, reason)
        await _send_message(ctx, user, ctx.author, id, 'unban')
    except Exception as e:
        print(e)
        CustomError('Error al desbannear')

    pass


async def _send_message(ctx: Context, user: User, author: User, id, type: str, time=None):
    message = f':white_check_mark: `#{id}` <@!{user.id}>, '
    if type == 'warn':
        message += 'tómatelo como una advertencia y que no se repita.'
        pass
    elif type == 'mute':
        message += 'muteado'
        pass
    elif type == 'kick':
        message += 'fuera de aquí, escoria'
        pass
    elif type == 'ban':
        message += 'reúnete con la Muerte a través de mis llamas.'
        pass
    elif type == 'unban':
        message += 'puedes resurgir entre tus cenizas.'
    else:
        raise CustomError('Invalid Punishment')

    await ctx.send(message)
