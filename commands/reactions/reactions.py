import discord
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord.ext.commands import Bot, Cog, Context, command, check_any
from commands.reactions.commands.command import Command
from commands.admin.commands.checks import is_admin, is_enabled_channel, _is_enabled_channel

class Reacciones(Cog):
    def __init__(self, bot: Bot):
        if not hasattr(bot, "slash"):
            # Creates new SlashCommand instance to bot if bot doesn't have.
            bot.slash = SlashCommand(bot, override_type=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    # @command(name='hug')
    # @check_any(is_enabled_channel())
    # async def hug(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='hug', descripcion=' hugged ')
    #
    # @cog_ext.cog_slash(name="hug")
    # @check_any(is_enabled_channel())
    # async def _hug(self, ctx: SlashContext):
    #     return await Comando(ctx=ctx, nombre='hug', descripcion=' hugged ')
    #
    # @command(name='lick')
    # @check_any(is_enabled_channel())
    # async def lick(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='lick', descripcion=' licked ')
    #
    # @cog_ext.cog_slash(name="lick")
    # @check_any(is_enabled_channel())
    # async def _lick(self, ctx: SlashContext):
    #     return await Comando(ctx=ctx, nombre='lick', descripcion=' licked ')
    #
    # @command(name='felicidades', aliases=['congrats', 'congratulations'])
    # @check_any(is_enabled_channel())
    # async def felicidades(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='felicidades', descripcion=' felicitó a ')
    #
    # @cog_ext.cog_slash(name="felicidades")
    # @check_any(is_enabled_channel())
    # async def _felicidades(self, ctx: SlashContext):
    #     return await Comando(ctx=ctx, nombre='felicidades', descripcion=' felicitó a ')
    #
    # @command(name='echaragua')
    # @check_any(is_enabled_channel())
    # async def echaragua(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='echaragua', descripcion=' ha mojado a ')
    #
    # @cog_ext.cog_slash(name="echaragua")
    # @check_any(is_enabled_channel())
    # async def _echaragua(self, ctx: SlashContext):
    #     return await Comando(ctx=ctx, nombre='echaragua', descripcion=' ha mojado a ')
    #
    # @command(name='felizcumple')
    # @check_any(is_enabled_channel())
    # async def felizcumple(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='felizcumple', descripcion=' felicitó a ')
    #
    # @cog_ext.cog_slash(name="felizcumple")
    # @check_any(is_enabled_channel())
    # async def _felizcumple(self, ctx: SlashContext):
    #     return await Comando(ctx=ctx, nombre='felizcumple', descripcion=' felicitó a ')
    #
    # @command(name='nalgada')
    # @check_any(is_enabled_channel())
    # async def nalgada(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='nalgada', descripcion=' le dio unas buenas nalgadas a ')
    #
    # @cog_ext.cog_slash(name="nalgada")
    # @check_any(is_enabled_channel())
    # async def _nalgada(self, ctx: SlashContext):
    #     return await Comando(ctx=ctx, nombre='nalgada', descripcion=' le dio unas buenas nalgadas a ')

    @Cog.listener()
    async def on_message(self, message):
        if not await _is_enabled_channel(message):
            return

        if message.author.id == self.bot.user.id or message.author.bot:
            return

        n_comando = " ".join(message.content.split(" ")[:1])

        if len(n_comando) > 0 and n_comando[0] == self.bot.command_prefix:
            n_comando = n_comando[1:]
        else:
            return

        return await Command(message=message, nombre=n_comando)

def setup(bot: Bot) -> None:
    bot.add_cog(Reacciones(bot))
