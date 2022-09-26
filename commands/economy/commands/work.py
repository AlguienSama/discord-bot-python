import random
from discord.ext.commands import Context
from utils.ddbb.economy import update_work
from utils.responses.Embed import Embed


async def work(ctx: Context):

    money = random.randint(1000, 2000)
    await update_work(ctx.guild.id, ctx.author.id, money)

    embed = Embed(title='Work', description=f'Has obtenido **{money:,}** haikoins', user=ctx.author) \
        .economy().get_embed()

    return await ctx.send(embed=embed)
