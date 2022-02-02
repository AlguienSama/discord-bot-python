from discord_slash import cog_ext
from discord.ext.commands import *
from commands.admin.commands.checks import is_admin
from .commands.commands import *


class Settings(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='enable')
    @check_any(is_admin())
    async def enable(self, ctx: Context, command: str, *channels):
        """ """
        await enable(ctx, command, channels)

    @command(name='disable')
    @check_any(is_admin())
    async def disable(self, ctx: Context, command: str, *channels):
        """ """
        await disable(ctx, command, channels)


def setup(bot: Bot) -> None:
    bot.add_cog(Settings(bot))