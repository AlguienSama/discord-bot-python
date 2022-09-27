import random
from discord.ext.commands import Context
from utils.logs.economy import log_work
from utils.responses.Embed import Embed


async def work(ctx: Context):
    money = random.randint(1000, 2000)
    await log_work(ctx, money)
    embed = Embed(title='Work', description=f'Has obtenido **{money:,}** haikoins', user=ctx.author).economy().get_embed()
    return await ctx.send(embed=embed)
