import json
import discord
import datetime

from firebase_admin import firestore
from discord.ext.commands import Bot, Context
from discord_slash import SlashContext
from disputils import BotEmbedPaginator, BotConfirmation
from utils.responses.Embed import Embed
from utils.ddbb.DB import get_admin_channels


db = firestore.client()


async def canalesPermitidos(ctx):
    args = ctx.message.content.split(" ")[1:]

    if len(args) < 1:
        return await ctx.send("Faltan parametros./ <#canal1> <#canal2> ... <#canaln>")

    channels = []
    error = ''
    for i in range(0, len(args)):
        try:
            channels.append(int(str(args[i]).replace('<#', '').replace('!', '').replace('>', '')))

        except:
            error = error + "`{}` no es valido.\n".format(args[i])

    if error != '':
        return await ctx.send(error)

    doc_ref = await get_admin_channels(str(ctx.message.guild.id))
    admin_channels = doc_ref.get()

    ids_channels = []
    sw = False
    if admin_channels.to_dict() is not None and ('ids' in admin_channels.to_dict()):
        ids_channels = admin_channels.to_dict()['ids']
        sw = True

    ids_guardados = []

    for id_canal in channels:
        if not (id_canal in ids_channels):
           ids_channels.append(id_canal)
           ids_guardados.append(id_canal)

    if sw:
        doc_ref.update({
            'ids': ids_channels
        })
    else:
        doc_ref.set({
            'ids': ids_channels
        })

    embed = discord.Embed()
    embed.title = "Canales Permitidos"
    embed.description = "Canal(es) {} guardado(s).".format('-' if len(ids_guardados) == 0 else "<#" +
                        (">, <#".join(str(c) for c in ids_guardados))+">")

    # si el comando se llama normalmente
    if type(ctx) == Context:
        return await ctx.send(embed=embed)

    # si el comando se llama por Slash
    elif type(ctx) == SlashContext:
        return await ctx.send(embeds=[embed])


async def quitarCanalesPermitidos(ctx):
    args = ctx.message.content.split(" ")[1:]

    if len(args) < 1:
        return await ctx.send("Faltan parametros./ <#canal1> <#canal2> ... <#canaln>")

    channels = []
    error = ''
    for i in range(0, len(args)):
        try:
            channels.append(int(str(args[i]).replace('<#', '').replace('!', '').replace('>', '')))

        except:
            error = error + "`{}` no es valido.\n".format(args[i])

    if error != '':
        return await ctx.send(error)

    doc_ref = await get_admin_channels(str(ctx.message.guild.id))
    admin_channels = doc_ref.get()

    ids_channels = []
    sw = False
    if admin_channels.to_dict() is not None and ('ids' in admin_channels.to_dict()):
        ids_channels = admin_channels.to_dict()['ids']
        sw = True

    ids_borrados = []

    for id_canal in channels:
        if id_canal in ids_channels:
           ids_channels.remove(id_canal)
           ids_borrados.append(id_canal)

    if sw:
        doc_ref.update({
            'ids': ids_channels
        })
    else:
        doc_ref.set({
            'ids': ids_channels
        })

    embed = discord.Embed()
    embed.title = "Canales Permitidos"
    embed.description = "Canal(es) {} removido(s).".format('-' if len(ids_borrados) == 0 else "<#" +
                        (">, <#".join(str(c) for c in ids_borrados))+">")

    # si el comando se llama normalmente
    if type(ctx) == Context:
        return await ctx.send(embed=embed)

    # si el comando se llama por Slash
    elif type(ctx) == SlashContext:
        return await ctx.send(embeds=[embed])


async def listaCanalesPermitidos(ctx):
    doc_ref = await get_admin_channels(str(ctx.message.guild.id))
    admin_channels = doc_ref.get()

    if admin_channels.to_dict() is not None and ('ids' in admin_channels.to_dict()):
        channels = admin_channels.to_dict()['ids']

        embed = discord.Embed()
        embed.title = "Canales Permitidos"
        Embeds = []
        con = 0
        np = 10
        embed.description = ''
        for c in channels:
            con = con + 1
            embed.description = embed.description + '`{}` - <#{}>\n'.format(con if con >= 10 else '0'+str(con), c)
            if con >= np or channels[len(channels) - 1] == c:
                con = 0
                Embeds.append(embed)
                embed = discord.Embed()
                embed.title = "Canales Permitidos"
                embed.description = ''

        paginator = BotEmbedPaginator(ctx, Embeds)
        await paginator.run()

    else:
        return await ctx.send("No hay restricción de canales en este servidor.")
