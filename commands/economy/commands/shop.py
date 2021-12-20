from discord.ext.commands import Context
from disputils import BotEmbedPaginator

from utils.ddbb.economy import get_items

async def shop(ctx: Context, category = None):
    items = await get_items(ctx.guild.id)