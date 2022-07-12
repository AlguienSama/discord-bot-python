from discord.ext.commands import Bot, Cog, Context, command, check
from firebase_admin import firestore
from utils.ddbb.DB import get_admin_channels, get_disabled_command

db = firestore.client()


def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id

    return check(predicate)


def is_admin():
    async def predicate(ctx):
        # if not ctx.author.guild_permissions.administrator:
        #    await ctx.send("no tienes permiso para ejecutar este comando")

        return ctx.author.guild_permissions.administrator

    return check(predicate)


def is_enabled_channel():
    async def predicate(ctx):
        doc_ref = await get_admin_channels(str(ctx.message.guild.id))
        admin_channels = doc_ref.get()

        if admin_channels.to_dict() is not None and ('ids' in admin_channels.to_dict()):
            channels = admin_channels.to_dict()['ids']
            return ctx.message.channel.id in channels

        else:
            return True

    return check(predicate)


async def _is_enabled_channel(message):
    try: 
        doc_ref = await get_admin_channels(str(message.guild.id))
        admin_channels = None
        try: 
            admin_channels = doc_ref.get()
        except Exception as e:
            print('Error: ' + str(e))

        if admin_channels.to_dict() is not None and ('ids' in admin_channels.to_dict()):
            channels = admin_channels.to_dict()['ids']
            return message.channel.id in channels

        else:
            return True
    except:
        return True


async def is_disabled_command(ctx: Context):
    if not hasattr(ctx, 'command'):
        return False

    doc_ref = await get_disabled_command(ctx.guild.id, ctx.command)
    channels = doc_ref.get()
    channels = channels.to_dict()

    if channels is not None and ('channels' in channels):
        return str(ctx.channel.id) in channels['channels']
    else:
        return False
