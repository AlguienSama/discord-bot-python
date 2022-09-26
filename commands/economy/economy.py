from discord.ext.commands import *
from .commands.balance import balance
from .commands.work import work
from .commands.casino import *
from .commands.haikoins import *
from .commands.shop_items import *


class Economy(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    @command(name='bal', description="Ver tu balance de monedas")
    async def bal(self, ctx: Context, user=None):
        """ """
        return await balance(ctx, user)

    @command(name='work', description="Obtener monedas gratuitas")
    async def work(self, ctx: Context):
        """ """
        return await work(ctx)

    @command(name='flip', description="Apostar dinero (50% de duplicar o perder)")
    async def flip(self, ctx: Context, bal):
        """ """
        return await flip(ctx, int(bal))

    @command(name='haikoin', aliases=['haikoins'], description="Haikoins obtenidos")
    async def _haikoin(self, ctx: Context, user=None):
        """ """
        return await get_haikoin(ctx, user)

    @command(name='item-create', description="Crear un objeto")
    async def _create_item(self, ctx: Context):
        """ """
        return await item_create(ctx)

    @command(name='roulette', aliases=['ruleta', 'r'], description="Ruleta del casino")
    async def _join_roulette(self, ctx: Context, money: int, *args):
        """ """
        return await join_roulette(self.bot, ctx, money, args)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Economy(bot))
