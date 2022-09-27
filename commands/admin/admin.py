import discord
from discord.ext.commands import Bot, Cog, Context, command, check_any, is_owner
from commands.admin.commands.experiencia import Metas, ListaMetas, EliminarMeta, CanalMeta, RemoveExp, AddExp, ResetExp
from commands.admin.commands.canales import canalesPermitidos, quitarCanalesPermitidos, listaCanalesPermitidos
from commands.admin.commands.checks import is_admin, is_guild_owner
from commands.admin.commands.reaction_commands import add_command, remove_command, lista_comandos
from commands.admin.commands.commands import enable, disable
from .commands.economy import *


class Administration(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='xp-metas', aliases=['metas', 'xpm'], description='Comando para administrar las metas de experiencia')
    @check_any(is_admin())
    async def metasXp(self, ctx: Context):
        """ """
        return await Metas(ctx=ctx)

    @command(name='xp-ml', aliases=['xpml'], description="Listado de las metas de experiencia en el servidor")
    @check_any(is_admin())
    async def metasLXp(self, ctx: Context):
        """ """
        return await ListaMetas(ctx=ctx)

    @command(name='xp-mdel', aliases=['xpdel', 'xpmdel', 'xpmd'], description="Elimina una meta de experiencia")
    @check_any(is_admin())
    async def metasDXp(self, ctx: Context):
        """ """
        return await EliminarMeta(ctx=ctx)

    @command(name='xp-mcanal', aliases=['xpcanal', 'xpmcanal', 'xpmc'], description="Asigna un canal para mostrar las metas de experiencia")
    @check_any(is_admin())
    async def metasCXp(self, ctx: Context):
        """ """
        return await CanalMeta(ctx=ctx)

    @command(name='xp-add', aliases=['xpa'], description="Añade experiencia a un usuario")
    @check_any(is_admin())
    async def addExp(self, ctx: Context):
        """ """
        return await AddExp(ctx=ctx)

    @command(name='xp-remove', aliases=['xpr'], description="Elimina la experiencia de un usuario")
    @check_any(is_admin())
    async def removeExp(self, ctx: Context):
        """ """
        return await RemoveExp(ctx=ctx)

    @command(name='xp-reset', description="Resetea la experiencia de un usuario")
    @check_any(is_guild_owner())
    async def resetExp(self, ctx: Context):
        """ """
        return await ResetExp(ctx=ctx)

    @command(name='enablechannel', aliases=['enac'], description="Permite que el bot pueda usar un canal")
    @check_any(is_admin())
    async def enableChannel(self, ctx: Context):
        """ """
        return await canalesPermitidos(ctx=ctx)

    @command(name='disablechannel', aliases=['disc'], description="Desactiva un canal para el bot")
    @check_any(is_admin())
    async def removeEnableChannel(self, ctx: Context):
        """ """
        return await quitarCanalesPermitidos(ctx=ctx)

    @command(name='lista-enablechannel', aliases=['l-ec'], description="Lista los canales permitidos")
    @check_any(is_admin())
    async def listaEnableChannel(self, ctx: Context):
        """ """
        return await listaCanalesPermitidos(ctx=ctx)

    @command(name='enable-command', aliases=['encom'], description="Permite que el bot pueda usar un comando")
    @check_any(is_admin())
    async def enable(self, ctx: Context, command: str, *channels):
        """ """
        await enable(ctx, command, channels)

    @command(name='disable', aliases=['discom'], description="Desactiva un comando para el bot")
    @check_any(is_admin())
    async def disable(self, ctx: Context, command: str, *channels):
        """ """
        await disable(ctx, command, channels)

    @command(name='add-command', description='Añadir un nuevo comando', help='<command> <link> [color, text]')
    @is_owner()
    async def _add_command(self, ctx: Context, command, link, *args):
        """ """
        return await add_command(ctx=ctx, cmd=command, img=link, args=args)

    @command(name='remove-command', description='Elimina un comando por id', help='<command> <id>')
    @is_owner()
    async def _remove_command(self, ctx: Context, command, id):
        """ """
        return await remove_command(ctx=ctx, cmd=command, id=id)

    @command(name='list-command', description='Lista de los comandos')
    @is_owner()
    async def _lista_comandos(self, ctx: Context, command=None, id=None):
        """ """
        return await lista_comandos(ctx=ctx, cmd=command, id=id)

    @command(name='add-money', description='Añadir dinero a un usuario', help='<user> <money>')
    @check_any(is_admin())
    async def _add_money(self, ctx: Context, user: discord.User, money: int):
        """ """
        return await add_money(ctx, user, money)

    @command(name='remove-money', description='Quitar dinero a un usuario', help='<user> <money>')
    @check_any(is_admin())
    async def _remove_money(self, ctx: Context, user: discord.User, money: int):
        """ """
        return await remove_money(ctx, user, money)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Administration(bot))
