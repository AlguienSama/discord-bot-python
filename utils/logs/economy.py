import discord
from discord.ext.commands import *
from utils.responses.Embed import Embed
from utils.ddbb.economy import *
from utils.ddbb.DB import __get__, __set__


async def _send(ctx: Context, embed: discord.Embed):
    channel = 782309852910977154  # TODO: DDBB query
    try:
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


async def win_money(ctx: Context, user: discord.User, money: int, type: str):
    await update_bal(ctx.guild.id, user.id, money)
    embed = Embed(title=type, user=user, description=f'{user.id} ha ganado {money} en {ctx.channel.id}') \
        .success()

    await _send(ctx, embed.get_embed())


async def lose_money(ctx: Context, user: discord.User, money: int, type: str):
    await update_bal_negative(ctx.guild.id, user.id, money)
    embed = Embed(title=type, user=user, description=f'{user.id} ha ganado {money} en {ctx.channel.id}') \
        .failure()

    await _send(ctx, embed.get_embed())
