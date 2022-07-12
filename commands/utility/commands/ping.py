from discord.ext.commands import Bot, Context
from utils.responses.Embed import Embed


async def GetPing(bot: Bot, ctx: Context):
    p = int(round(bot.latency, 3) * 1000)
    embed = Embed(description=":satellite: Pong! **{0}ms.**".format(p))

    if p > 300:
        embed.failure()

    elif p > 150:
        embed.color = 0xffcc00

    else:
        embed.success()


    # si el comando se llama normalmente
    if type(ctx) == Context:
        return await ctx.send(embed=embed.get_embed())
