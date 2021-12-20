from utils.errors import CustomError
from discord.ext.commands import Context, TextChannelConverter


async def say(ctx: Context, *, message: str):
    if message is None:
        raise CustomError('Que mensaje quieres que diga?')

    channel = ctx.channel

    message = message.split(' ')
    try:
        channel = await TextChannelConverter().convert(ctx, message[0])
        message = message[1:]
    except:
        pass

    message = ' '.join(message)
    await channel.send(message)
