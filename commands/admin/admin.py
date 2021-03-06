from discord.ext.commands import Bot, Cog, Context, command, check_any, is_owner
from commands.admin.commands.experiencia import Metas, ListaMetas, EliminarMeta, CanalMeta, RemoveExp, AddExp, ResetExp
from commands.admin.commands.canales import canalesPermitidos, quitarCanalesPermitidos, listaCanalesPermitidos
from commands.admin.commands.checks import is_admin, is_guild_owner
from commands.admin.commands.commands import add_command, remove_command, lista_comandos
from .commands.economy import *


class Admin(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='xp-metas', aliases=['metas', 'xpm'])
    @check_any(is_admin())
    async def metasXp(self, ctx: Context):
        """ """
        return await Metas(ctx=ctx)

    @command(name='xp-ml', aliases=['xpml'])
    @check_any(is_admin())
    async def metasLXp(self, ctx: Context):
        """ """
        return await ListaMetas(ctx=ctx)

    @command(name='xp-mdel', aliases=['xpdel', 'xpmdel', 'xpmd'])
    @check_any(is_admin())
    async def metasDXp(self, ctx: Context):
        """ """
        return await EliminarMeta(ctx=ctx)

    @command(name='xp-mcanal', aliases=['xpcanal', 'xpmcanal', 'xpmc'])
    @check_any(is_admin())
    async def metasCXp(self, ctx: Context):
        """ """
        return await CanalMeta(ctx=ctx)

    @command(name='xp-remove', aliases=['xpr'])
    @check_any(is_admin())
    async def removeExp(self, ctx: Context):
        """ """
        return await RemoveExp(ctx=ctx)

    @command(name='xp-add', aliases=['xpa'])
    @check_any(is_admin())
    async def addExp(self, ctx: Context):
        """ """
        return await AddExp(ctx=ctx)

    @command(name='enablechannel', aliases=['ec'])
    @check_any(is_admin())
    async def enableChannel(self, ctx: Context):
        """ """
        return await canalesPermitidos(ctx=ctx)

    @command(name='remove-enablechannel', aliases=['r-ec'])
    @check_any(is_admin())
    async def removeEnableChannel(self, ctx: Context):
        """ """
        return await quitarCanalesPermitidos(ctx=ctx)

    @command(name='lista-enablechannel', aliases=['l-ec'])
    @check_any(is_admin())
    async def listaEnableChannel(self, ctx: Context):
        """ """
        return await listaCanalesPermitidos(ctx=ctx)

    @command(name='reset-xp')
    @check_any(is_guild_owner())
    async def resetExp(self, ctx: Context):
        """ """
        return await ResetExp(ctx=ctx)

    @command(name='add-command', description='A??adir un nuevo comando', help='<command> <link> [color, text]')
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

    @command(name='add-money', description='A??adir dinero a un usuario', help='<user> <money>')
    @check_any(is_admin())
    async def _add_money(self, ctx: Context, user, money: int):
        """ """
        return await add_money(ctx, user, money)

    @command(name='remove-money', description='Quitar dinero a un usuario', help='<user> <money>')
    @check_any(is_admin())
    async def _remove_money(self, ctx: Context, user, money: int):
        """ """
        return await remove_money(ctx, user, money)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Admin(bot))
