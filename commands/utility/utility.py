from discord.ext.commands import Bot, Cog, Context, command, check_any, is_owner, cooldown, BucketType
from .commands.ping import GetPing
from .commands.say import say
from .commands.server import server
from .commands.chatgpt import openai_chatgpt
from .commands.exp import experiencia, getExp, rank_xp
from .commands.AI import colorizer, super_resolution, waifu2x, text_to_image, toonify
from commands.admin.commands.checks import is_enabled_channel, _is_enabled_channel, is_disabled_command
from commands.together.commands.discord_together import *
import os


class Utiles(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='ping', description="Envía un ping al servidor")
    @check_any(is_enabled_channel())
    async def ping(self, ctx: Context):
        """Ping del bot al host de discord"""
        return await GetPing(self.bot, ctx=ctx)

    @Cog.listener()
    async def on_message(self, message):
        if not await _is_enabled_channel(message):
            return
        if await is_disabled_command(ctx=message):
            return

        if message.author.id == self.bot.user.id or message.author.bot:
            return

        return await experiencia(message)

    @command(name='xp', description="Ver la experiencia de un usuario")
    @check_any(is_enabled_channel())
    async def xp(self, ctx: Context):
        """ """
        return await getExp(ctx=ctx)

    @command(name='rank', description="Ver el ranking de experiencia en el servidor")
    @check_any(is_enabled_channel())
    async def _rank_xp(self, ctx: Context):
        """ """
        return await rank_xp(self.bot, ctx=ctx)

    @command(name='colorear', description="Colorear una imagen")
    @check_any(is_enabled_channel())
    async def _colorizer(self, ctx: Context, link):
        """ """
        return await colorizer(ctx=ctx, link=link)

    @command(name='super_resolution', description="Aumentar la resolución de una imagen")
    @check_any(is_enabled_channel())
    async def _super_resolution(self, ctx: Context, link):
        """ """
        return await super_resolution(ctx=ctx, link=link)

    @command(name='waifu2x', description="Aumentar la resolución de una imagen")
    @check_any(is_enabled_channel())
    async def _waifu2x(self, ctx: Context, link):
        """ """
        return await waifu2x(ctx=ctx, link=link)

    @command(name='text2image', description="Aumentar la resolución de una imagen")
    @check_any(is_enabled_channel())
    async def _text_to_image(self, ctx: Context, *args):
        """ """
        return await text_to_image(ctx=ctx, args=args)

    @command(name='toonify', description="Editar una imagen con IA")
    @check_any(is_enabled_channel())
    async def _toonify(self, ctx: Context, link):
        """ """
        return await toonify(ctx=ctx, link=link)

    @command(name='say', description="Hacer que el bot diga algo")
    @check_any(is_enabled_channel(), is_owner())
    async def _say(self, ctx: Context, *, message=None):
        """ """
        return await say(ctx=ctx, message=message)

    @command(name='server', alias=['server_info'], description="Información del servidor")
    @check_any(is_enabled_channel())
    async def _server(self, ctx: Context):
        """ """
        return await server(ctx)

    @command(name = "ask", alias=['aurora', 'pregunta'], description = "Haz una pregunta al bot")
    @cooldown(1, os.getenv("OPENAI_CD"), BucketType.channel)
    async def _openai_chatgpt (self, ctx: Context, *, question: str):
        """ """
        return await openai_chatgpt(ctx, question)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Utiles(bot))
