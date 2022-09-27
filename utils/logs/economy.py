import discord
from discord.ext.commands import *
from utils.responses.Embed import Embed
from utils.ddbb.economy import *
from utils.ddbb.DB import __get__, __set__


async def _send(ctx: Context, embed: discord.Embed):
    channel = 649003749439701012  # TODO: DDBB query
    try:
        if ctx.guild.id == 782035590501498900:
            channel = 945371397847404554
        await ctx.guild.get_channel(channel).send(embed=embed)
    except:
        # Para pruebas en otros servers hasta que no se tenga la ddbb lista
        try:
            await ctx.guild.get_channel(649003749439701012).send(embed=embed)
        except:
            try:
                await ctx.guild.get_channel(815678509422215198).send(embed=embed)
            except:
                pass
            pass
        pass

def msg(ctx: discord.ext.commands.Context, user: discord.User, money: int, win: bool):
    return f'User: {user.mention}\nUser ID: **{user.id}**\nAcción: **{"Ganar" if win else "Perder"}**\nCantidad: **{money:,}**\nCanal: {ctx.channel.mention} **{ctx.channel.id}**'

async def win_money(ctx: Context, user: discord.User, money: int, type: str):
    await update_bal(ctx.guild.id, user.id, money)
    embed = Embed(title=type, user=user, description=msg(ctx, user, money, True)).success()
    await _send(ctx, embed.get_embed())


async def lose_money(ctx: Context, user: discord.User, money: int, type: str):
    await update_bal_negative(ctx.guild.id, user.id, money)
    embed = Embed(title=type, user=user, description=msg(ctx, user, money, False)).failure()
    await _send(ctx, embed.get_embed())

async def log_work(ctx: Context, money: int):
    user = ctx.author
    await update_work(ctx.guild.id, user.id, money)
    embed = Embed(title='Work', user=user, description=msg(ctx, user, money, True)).success()
    await _send(ctx, embed.get_embed())