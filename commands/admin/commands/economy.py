from discord.ext.commands import Context, UserConverter
from disputils import BotConfirmation
from utils.responses.Embed import Embed
from utils.ddbb.economy import *


async def add_money(ctx: Context, user, money: int):
    try:
        user = await UserConverter().convert(ctx, user)
    except:
        user = ctx.author

    confirmation = BotConfirmation(ctx=ctx, color=0x012345)
    await confirmation.confirm(f'¿Quieres agregar {money} haikoins a {user} ?')

    if confirmation.confirmed:
        await update_bal(ctx.guild.id, user.id, money)
        return await confirmation.update(f'Se han añadido {money} haikoins a {user}!!', hide_author=False, color=0x55ff55)
    else:
        return await confirmation.update("Cancelado...", hide_author=False, color=0xff5555)


async def remove_money(ctx: Context, user, money: int):
    try:
        user = await UserConverter().convert(ctx, user)
    except:
        user = ctx.author

    confirmation = BotConfirmation(ctx=ctx, color=0x012345)
    await confirmation.confirm(f'¿Quieres quitar {money} haikoins a {user} ?')

    if confirmation.confirmed:
        await update_bal(ctx.guild.id, user.id, money*-1)
        return await confirmation.update(f'Se han quitado {money} haikoins a {user}!!', hide_author=False, color=0x55ff55)
    else:
        return await confirmation.update("Cancelado...", hide_author=False, color=0xff5555)
