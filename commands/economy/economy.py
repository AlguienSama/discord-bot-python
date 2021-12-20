from discord_slash import SlashCommand
from discord.ext.commands import *
from .commands.balance import balance
from .commands.work import work
from .commands.casino import *
from .commands.haikoins import *


class Economy(Cog):
    def __init__(self, bot: Bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @command(name='bal')
    async def bal(self, ctx: Context, user=None):
        """ """
        return await balance(ctx, user)

    @command(name='work')
    async def work(self, ctx: Context):
        """ """
        return await work(ctx)

    @command(name='flip')
    async def flip(self, ctx: Context, bal):
        """ """
        return await flip(ctx, int(bal))

    @command(name='haikoin', aliases=['haikoins'])
    async def _haikoin(self, ctx: Context, user=None):
        """ """
        return await get_haikoin(ctx, user)


def setup(bot: Bot) -> None:
    bot.add_cog(Economy(bot))
