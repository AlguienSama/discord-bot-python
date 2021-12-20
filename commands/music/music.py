from discord.ext.commands import Bot, Cog, command, check_any, Context
from discord_slash import SlashCommand

from commands.admin.commands.checks import is_admin
from commands.music.commands.music import join, play, queue, add_queue, skip


class Music(Cog):
    def __init__(self, bot: Bot):
        if not hasattr(bot, "slash"):
            # Creates new SlashCommand instance to bot if bot doesn't have.
            bot.slash = SlashCommand(bot, override_type=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    @command(name='join')
    async def _join(self, ctx: Context):
        """ """
        return await join(bot=self.bot, ctx=ctx)

    @command(name='play')
    async def _play(self, ctx: Context, url: str):
        """ """
        return await play(self.bot, ctx, url)

    @command(name='queue', aliases=['q'])
    async def _queue(self, ctx: Context):
        """ """
        return await queue(ctx)

    @command(name='add_queue', aliases=['aq'])
    async def _add_queue(self, ctx: Context, song: str):
        """ """
        return await add_queue(ctx, song)

    @command(name='skip')
    async def _skip(self, ctx: Context, first: int = 0, last: int = 0):
        """ """
        return await skip(self.bot, ctx, first, last)


def setup(bot: Bot) -> None:
    bot.add_cog(Music(bot))
