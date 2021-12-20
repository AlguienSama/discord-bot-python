import discord
from discord.ext.commands import *
from utils.responses.Embed import Embed
from utils.ddbb.DB import __get__, __set__


async def send(ctx: Context, embed: discord.Embed):
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


async def win(ctx: Context, user: discord.User, money: int, type: str):

    embed = Embed(title=type, user=user, description=f'{user.id} ha ganado {money} en {ctx.channel.id}') \
        .success()

    await send(ctx, embed.get_embed())


async def lose(ctx: Context, user: discord.User, money: int, type: str):
    embed = Embed(title=type, user=user, description=f'{user.id} ha ganado {money} en {ctx.channel.id}') \
        .failure()

    await send(ctx, embed.get_embed())
