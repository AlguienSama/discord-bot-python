from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord.ext.commands import Bot, Cog, Context, command, check_any, is_owner
from commands.utilidades.funciones.ping import GetPing
from commands.utilidades.funciones.say import say
from .funciones.server import server
from commands.utilidades.funciones.exp import experiencia, getExp, rank_xp
from commands.utilidades.funciones.AI import colorizer, super_resolution, waifu2x, text_to_image, toonify
from commands.admin.funciones.checks import is_enabled_channel, _is_enabled_channel, is_disabled_command
from commands.together.funciones.discord_together import *


class Utiles(Cog):
    def __init__(self, bot: Bot):
        if not hasattr(bot, "slash"):
            # Creates new SlashCommand instance to bot if bot doesn't have.
            bot.slash = SlashCommand(bot, override_type=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @command(name='ping')
    @check_any(is_enabled_channel())
    async def ping(self, ctx: Context):
        """Ping del bot al host de discord"""
        return await GetPing(self.bot, ctx=ctx)

    @cog_ext.cog_slash(name="ping")
    @check_any(is_enabled_channel())
    async def _ping(self, ctx: SlashContext):
        return await GetPing(self.bot, ctx=ctx)

    @Cog.listener()
    async def on_message(self, message):
        if not await _is_enabled_channel(message):
            return
        if await is_disabled_command(ctx=message):
            return

        if message.author.id == self.bot.user.id or message.author.bot:
            return

        #print("mensaje {}".format(message.author))
        return await experiencia(message)

    @command(name='xp')
    @check_any(is_enabled_channel())
    async def xp(self, ctx: Context):
        """ """
        return await getExp(ctx=ctx)

    @command(name='rank')
    @check_any(is_enabled_channel())
    async def _rank_xp(self, ctx: Context):
        """ """
        return await rank_xp(self.bot, ctx=ctx)

    @cog_ext.cog_slash(name="xp")
    @check_any(is_enabled_channel())
    async def _xp(self, ctx: SlashContext):
        return await getExp(ctx=ctx)

    @command(name='colorear')
    @check_any(is_enabled_channel())
    async def _colorizer(self, ctx: Context, link):
        """ """
        return await colorizer(ctx=ctx, link=link)

    @command(name='super_resolution')
    @check_any(is_enabled_channel())
    async def _super_resolution(self, ctx: Context, link):
        """ """
        return await super_resolution(ctx=ctx, link=link)

    @command(name='waifu2x')
    @check_any(is_enabled_channel())
    async def _waifu2x(self, ctx: Context, link):
        """ """
        return await waifu2x(ctx=ctx, link=link)

    @command(name='text2image')
    @check_any(is_enabled_channel())
    async def _text_to_image(self, ctx: Context, *args):
        """ """
        return await text_to_image(ctx=ctx, args=args)

    @command(name='toonify')
    @check_any(is_enabled_channel())
    async def _toonify(self, ctx: Context, link):
        """ """
        return await toonify(ctx=ctx, link=link)

    @command(name='say')
    @check_any(is_enabled_channel(), is_owner())
    async def _say(self, ctx: Context, *, message=None):
        """ """
        return await say(ctx=ctx, message=message)

    @command(name='server', alias=['server_info'])
    @check_any(is_enabled_channel())
    async def _server(self, ctx: Context):
        """ """
        return await server(ctx)


def setup(bot: Bot) -> None:
    bot.add_cog(Utiles(bot))
