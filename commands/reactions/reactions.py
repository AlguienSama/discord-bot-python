from discord.ext.commands import Bot, Cog
from commands.reactions.commands.command import Command
from commands.admin.commands.checks import _is_enabled_channel

class Reacciones(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # @command(name='hug', description="Dar un abrazo")
    # @check_any(is_enabled_channel())
    # async def hug(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='hug', descripcion=' hugged ')
    #
    # @command(name='lick', description="Lamer")
    # @check_any(is_enabled_channel())
    # async def lick(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='lick', descripcion=' licked ')
    #
    # @command(name='felicidades', aliases=['congrats', 'congratulations'], description="Felicitar")
    # @check_any(is_enabled_channel())
    # async def felicidades(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='felicidades', descripcion=' felicitó a ')
    #
    # @command(name='echaragua', description="Echar agua")
    # @check_any(is_enabled_channel())
    # async def echaragua(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='echaragua', descripcion=' ha mojado a ')
    #
    # @command(name='felizcumple', aliases=['happybirthday', 'happybirthday'], description="Desear feliz cumpleaños")
    # @check_any(is_enabled_channel())
    # async def felizcumple(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='felizcumple', descripcion=' felicitó a ')
    #
    # @command(name='nalgada', description="Dar una nalgada")
    # @check_any(is_enabled_channel())
    # async def nalgada(self, ctx: Context):
    #     """ """
    #     return await Comando(ctx=ctx, nombre='nalgada', descripcion=' le dio unas buenas nalgadas a ')

    @Cog.listener()
    async def on_message(self, message):
        if not await _is_enabled_channel(message):
            return
        if message.author.id == self.bot.user.id or message.author.bot:
            return

        try:
            prefix = await self.bot.get_prefix(message)
            for p in prefix:
                if message.content.startswith(p):
                    prefix = p
                    break
            if type(prefix) is list:
                return
            command = message.content.split(prefix)[1].split(' ')[0]
            return await Command(message=message, nombre=command)
        except Exception as e:
            print(e)
            return

async def setup(bot: Bot) -> None:
    await bot.add_cog(Reacciones(bot))
