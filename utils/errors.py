from discord.ext.commands import *
from datetime import datetime
from utils.responses.Embed import Embed

NoneType = type(None)


class TimeError(CommandError):
    def __init__(self, time: datetime):
        self.time = time


class MoneyError(CommandError):
    def __init__(self, min: int = None, max: int = None):
        self.min = min
        self.max = max


class NotMoneyError(CommandError):
    def __init__(self, money: int):
        self.money = money


class CommandNotExist(CommandError):
    def __init__(self, command: str):
        self.command = command


class CustomError(CommandError):
    def __init__(self, error):
        self.error = error


async def errors(ctx: Context, error):
    embed = Embed(ctx.author).failure()

    if isinstance(error, NotOwner):
        embed.description = 'Bot Owner Permissions Required'

    elif isinstance(error, UserNotFound):
        embed.description = 'Ningún usuario encontrado'

    elif isinstance(error, ChannelNotFound):
        embed.description = 'Ningún canal encontrado'

    elif isinstance(error, CommandNotFound):
        embed.description = 'Command Not Found'
        return

    elif isinstance(error, TimeoutError):
        embed.description = 'Fin del tiempo'

    elif isinstance(error, MissingRequiredArgument):
        embed.description = '**{}** es un argumento requerido'.format(error.param)
        embed.add_field('_ _', '{}\n`{}{} {}`'.format(ctx.command.description, ctx.prefix, ctx.command.name,
                                                        ctx.command.help))

    elif isinstance(error, MissingPermissions):
        print(error.missing_perms)
        embed.description = f'Permisos insuficientes `${error.missing_perms}`'

    elif isinstance(error, CheckAnyFailure):
        embed.description = 'Permisos insuficientes'

    elif isinstance(error, TimeError):
        embed.description = f'Faltan **{error.time}** para poder volver a ejecutar el comando'

    elif isinstance(error, MoneyError):
        msg = ''
        if error.min is not None:
            msg += f'Valor mínimo requerido: `{error.min}`'
        if error.min is not None and error.max is not None:
            msg += '\n'
        if error.max is not None:
            msg += f'Valo máximo requerido: `{error.max}`'
        embed.description = msg

    elif isinstance(error, NotMoneyError):
        embed.description = f'Te faltan {error.money} haikoins'

    elif isinstance(error, CommandNotExist):
        embed.description = f'El comando {error.command} no existe'

    elif isinstance(error, ValueError):
        embed.description = f'Debes de introducir un número válido'

    elif isinstance(error, CustomError):
        embed.description = error.error

    elif isinstance(error, CommandInvokeError):

        if isinstance(error.original, ValueError):
            embed.description = f'Debes de introducir los parámetros correctamente'
            embed.add_field('_ _', '{}\n`{}{} {}`'.format(ctx.command.description, ctx.prefix, ctx.command.name,
                                                            ctx.command.help))

        elif isinstance(error.original, NoneType):
            embed.description = f'Debes de introducir los parámetros correctamente'

        else:
            print(type(error))
            print(error)
            print(error.args)
            print(type(error.original))
            print(error.original)
            print(error.__context__)
            embed.description = 'Error al ejecutar un comando\n`{}`\n`{}`\nAvisa a un administrador'.format(error.args,
                                                                                                            error.original)

    else:
        embed.description = error.__class__.__name__

    return await ctx.send(embed=embed.get_embed())
