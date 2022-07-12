from discord.ext.commands import Bot, Cog, Context, command, check_any
from commands.admin.commands.checks import is_enabled_channel
from .commands.discord_together import *


class Together(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='youtube-together',
             description='Ver vídeos de youtube todos juntos en un chat de voz',
             help='youtube-together <voice channel>')
    @check_any(is_enabled_channel())
    async def _youtube_together(self, ctx: Context, channel):
        """ """
        return await youtube_together(ctx, channel)

    @command(name='poker-together',
             description='Poker',
             help='poker-together <voice channel>')
    @check_any(is_enabled_channel())
    async def _poker_together(self, ctx: Context, channel):
        """ """
        return await poker_together(ctx, channel)

    @command(name='betrayal-together',
             description='Como el among us',
             help='betrayal-together <voice channel>')
    @check_any(is_enabled_channel())
    async def _betrayal_together(self, ctx: Context, channel):
        """ """
        return await betrayal_together(ctx, channel)

    @command(name='fishing-together',
             description='Algo de pescar, yo que se',
             help='fishing-together <voice channel>')
    @check_any(is_enabled_channel())
    async def _fishing_together(self, ctx: Context, channel):
        """ """
        return await fishing_together(ctx, channel)

    @command(name='chess-together',
             aliases=['ajedrez'],
             description='Jugar al ajedrez en el chat de voz',
             help='chess-together <voice channel>')
    @check_any(is_enabled_channel())
    async def _chess_together(self, ctx: Context, channel):
        """ """
        return await chess_together(ctx, channel)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Together(bot))
