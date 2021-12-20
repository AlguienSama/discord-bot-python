from utils.responses.Embed import Embed
from discord.ext.commands import Context


async def send_cmd_help(ctx: Context):
    cmd = ctx.command
    embed = Embed()