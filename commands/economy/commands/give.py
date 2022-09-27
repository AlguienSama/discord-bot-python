import discord
from discord.ext.commands import Context, UserConverter, Us
from utils.errors import CustomError, MoneyError
from utils.responses.Embed import Embed
from utils.ddbb.economy import *
from utils.logs.economy import win_money, lose_money


async def give(ctx: Context, user: discord.User, money: int):
    try:
        user = await UserConverter().convert(ctx, user)
    except:
        raise CustomError('Usuario inválido')

    try:
        money = int(money)
        if money < 1:
            raise MoneyError(min=1)
    except:
        raise MoneyError(min=1)
    await check_bal(ctx.guild.id, ctx.author.id, money)
    
    await lose_money(ctx, ctx.author, money, f'Give to {user.id}')
    await win_money(ctx, user, money, f'Recive from {ctx.author.id}')
    
    embed = Embed(title='Donación', user=ctx.author, description=f'<@{ctx.author.id}> ha donado {money}💰 a <@{user.id}>').success()
    
    await ctx.channel.send(embed=embed)    
