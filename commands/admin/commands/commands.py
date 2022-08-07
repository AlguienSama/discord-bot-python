from discord.ext.commands import *

from utils.errors import CommandNotExist, CustomError
from utils.ddbb.DB import set_enabled_commands, set_disabled_commands
from utils.responses.Embed import Embed


async def enable(ctx: Context, command: str, channels):
    cmd = ctx.bot.get_command(name=command)

    if cmd is None:
        raise CommandNotExist(command)
    if ctx.command == command:
        raise CustomError('WTF bro')

    if not channels:
        print('a')
        channels = [str(ctx.channel.id)]

    print(channels)

    await set_enabled_commands(ctx.guild.id, command, channels)

    embed = Embed(description=f'Command {command} habilitado').success()
    await ctx.send(embed=embed.get_embed())


async def disable(ctx: Context, command: str, channels):
    cmd = ctx.bot.get_command(name=command)

    if cmd is None:
        raise CommandNotExist(command)
    if ctx.command == command:
        raise CustomError('WTF bro')

    if not channels:
        channels = [ctx.channel.id]

    await set_disabled_commands(ctx.guild.id, command, channels)

    embed = Embed(description=f'Command {command} deshabilitado').success()
    await ctx.send(embed=embed.get_embed())
