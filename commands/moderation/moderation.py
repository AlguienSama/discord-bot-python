from discord_slash import SlashCommand
from discord.ext.commands import *
from discord import User, Member
from .commands.punishment import *
from ..admin.commands.checks import is_admin


class Economy(Cog):
    def __init__(self, bot: Bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

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


def setup(bot: Bot) -> None:
    bot.add_cog(Economy(bot))