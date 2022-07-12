from discord.ext.commands import *
from discord import User
from .commands.punishment import *
from ..admin.commands.checks import is_admin


class Moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='warn')
    @check_any(is_admin())
    async def __warn(self, ctx: Context, user: User, *, reason=None):
        """ """
        return await warn(ctx, user, reason=reason)

    @command(name='kick')
    @check_any(is_admin())
    async def _kick(self, ctx: Context, user: User, *, reason=None):
        """ """
        return await kick(ctx, user, reason=reason)

    @command(name='ban')
    @check_any(is_admin())
    async def _ban(self, ctx: Context, user: User, *, reason=None):
        """ """
        return await ban(ctx, user, reason=reason)

    @command(name='unban')
    @check_any(is_admin())
    async def _unban(self, ctx: Context, user: User, *, reason=None):
        """ """
        return await unban(ctx, user, reason=reason)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Moderation(bot))