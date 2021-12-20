from discord.ext.commands import Context, UserConverter
from utils.responses.Embed import Embed
from utils.ddbb.economy import *


async def balance(ctx: Context, user=None):
    try:
        user = await UserConverter().convert(ctx, user)
    except:
        user = ctx.author

    bal = await get_bal(ctx.guild.id, user.id)
    bal = bal.get()
    bal = bal.to_dict()

    if bal is None:
        embed = Embed(user=user, description='Balance 💰') \
            .add_field('Haikoins:', '0', True) \
            .add_field('Inventory: ', 'Inventario vacío', True) \
            .economy()
    else:
        inventory = "\n".join(bal["inventory"]) if bal["inventory"] != [] else "Inventario vacío"
        embed = Embed(user=user, description='Balance 💰')\
            .add_field('Haikoins:', f'{bal["money"]:,}', True)\
            .add_field('Inventory: ', inventory, True)\
            .economy()

    await ctx.send(embed=embed.get_embed())
