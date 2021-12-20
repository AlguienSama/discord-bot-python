import random
from discord.ext.commands import Context
from utils.ddbb.economy import update_bal, check_bal
from utils.errors import MoneyError
from utils.responses.Embed import Embed
from utils.logs.economy import win


async def flip(ctx: Context, money: int):
    res = random.randint(0, 1)
    if money < 1:
        raise MoneyError(min=1)

    await check_bal(ctx.guild.id, ctx.author.id, money)

    embed = Embed(title='FLIP GAME')

    await win(ctx, ctx.author, money, 'Flip')

    if res == 0:
        money *= -1
        embed.description = f'Has perdido `{abs(money)}` haikoins!!'
        embed.failure()
    else:
        embed.description = f'Has ganado `{abs(money)}` haikoins!!'
        embed.success()
    await update_bal(ctx.guild.id, ctx.author.id, money)

    await ctx.send(embed=embed.get_embed())


async def join_roulette(ctx: Context, money: int, *args):
    if money < 1:
        raise MoneyError(min=1)

    await check_bal(ctx.guild.id, ctx.author.id, money)
