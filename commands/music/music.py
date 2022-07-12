from discord.ext.commands import Bot, Cog, command, Context

from commands.music.commands.music import join, play, queue, add_queue, skip


class Music(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

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


async def setup(bot: Bot) -> None:
    await bot.add_cog(Music(bot))
