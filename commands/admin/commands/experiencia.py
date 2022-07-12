import discord

from firebase_admin import firestore
from discord.ext.commands import Context
from disputils import BotEmbedPaginator, BotConfirmation
from utils.ddbb.DB import get_admin_xp, get_user_xp, delete_collection


db = firestore.client()


async def Metas(ctx):
    args = ctx.message.content.split(" ")[1:]

    if len(args) < 2:
        return await ctx.send("Faltan parametros./ <exp> <id rol>")

    doc_ref = await get_admin_xp(str(ctx.message.guild.id))
    admin_xp = doc_ref.get()
    mts = []
    idn = 1
    sw = False

    if admin_xp.to_dict() is not None and ('metas' in admin_xp.to_dict()) and \
            ('idcon' in admin_xp.to_dict()):
        mts = admin_xp.to_dict()['metas']
        idn = admin_xp.to_dict()['idcon'] + 1
        sw = True

    try:
        args[0] = int(args[0])
    except:
        return await ctx.send("Parametros incorrectos./ <exp> <id rol>")

    if type(args[0]) == int:
        if len(args) > 2 and args[2] is not None:
            msg = ' '.join(args[2:])
            mts.append({"id": idn, "exp": args[0], "rol": args[1], "msg": msg})
        else:
            mts.append({"id": idn, "exp": args[0], "rol": args[1]})

        if sw or (admin_xp.to_dict() is not None):
            doc_ref.update({
                'idcon': idn,
                'metas': mts,
            })
        else:
            doc_ref.set({
                'idcon': idn,
                'metas': mts
            })

        embed = discord.Embed()
        embed.title = "Metas"
        embed.description = "Meta `{}` guardada.".format(idn)

        # si el comando se llama normalmente
        if type(ctx) == Context:
            return await ctx.send(embed=embed)

    else:
        return await ctx.send("Parametros incorrectos./ <exp> <id rol>")


async def ListaMetas(ctx):
    doc_ref = await get_admin_xp(str(ctx.message.guild.id))
    admin_xp = doc_ref.get()

    if admin_xp.to_dict() is not None and ('metas' in admin_xp.to_dict()):
        mts = admin_xp.to_dict()['metas']

        embed = discord.Embed()
        embed.title = "Metas"
        Embeds = []
        con = 0
        np = 5
        for m in mts:
            con = con + 1
            text01 = '`Rol:` <@&' + str(m['rol']) + '> `' + str(m['rol'] + '`\n') + \
                     '`Exp:` ' + str(m['exp']) + '\n`Msg:` ' + (m['msg'] if 'msg' in m else '')
            embed.add_field(name='ID: `#{}`'.format(m['id']), value=text01, inline=False)
            if con >= np or mts[len(mts)-1] == m:
                con = 0
                Embeds.append(embed)
                embed = discord.Embed()
                embed.title = "Metas"

        paginator = BotEmbedPaginator(ctx, Embeds)
        await paginator.run()

    else:
        return await ctx.send("No hay metas en este servidor.")


async def EliminarMeta(ctx):
    args = ctx.message.content.split(" ")[1:]

    if len(args) < 1:
        return await ctx.send("Faltan parametros./ <ID de la meta> (solo numeros)")

    doc_ref = await get_admin_xp(str(ctx.message.guild.id))
    admin_xp = doc_ref.get()
    mts = []
    idn = 1
    sw = False

    try:
        args[0] = int(args[0])
    except:
        return await ctx.send("Parametros incorrectos./ <ID de la meta> (solo numeros)")

    if admin_xp.to_dict() is not None and ('metas' in admin_xp.to_dict()):
        mts = admin_xp.to_dict()['metas']
        con = 0
        sw = False

        for m in mts:
            if m['id'] == args[0]:
                sw = True
                break
            else:
                con = con + 1

        if sw:
            confirmation = BotConfirmation(ctx=ctx, color=0x012345)
            await confirmation.confirm("Estas seguro de eliminar la Meta `#{}`?".format(args[0]))

            if confirmation.confirmed:
                mts.pop(con)
                doc_ref.update({
                    'metas': mts,
                })
                txt = "Meta Eliminada Con Exito Por <@{}>".format(ctx.message.author.id)
                return await confirmation.update(txt, color=0x55ff55)
            else:
                return await confirmation.update("Cancelado...", hide_author=True, color=0xff5555)
        else:
            return await ctx.send("No se encontro la meta `{}`".format(args[0]))

    else:
        return ctx.send("No hay metas en este servidor.")


async def CanalMeta(ctx):
    args = ctx.message.content.split(" ")[1:]
    if len(args) < 1:
        return await ctx.send("Faltan parametros./ <ID del Canal / DM / None / Normal>")

    args[0] = str(args[0]).replace('<#', '').replace('>', '')

    doc_ref = await get_admin_xp(str(ctx.message.guild.id))
    admin_xp = doc_ref.get()

    try:
        n = int(args[0])
    except:
        if str(args[0]).lower() != 'dm' and str(args[0]).lower() != 'none' and str(args[0]).lower() != 'normal':
            return await ctx.send("Parametros incorrectos./ <ID del Canal / DM / None / Normal>")

    if admin_xp.to_dict() is not None:
        doc_ref.update({
            'canal': str(args[0]).lower()
        })
    else:
        doc_ref.set({
            'canal': str(args[0]).lower()
        })

    return await ctx.send("Guardado...")


async def RemoveExp(ctx):
    args = ctx.message.content.split(" ")[1:]
    if len(args) < 2:
        return await ctx.send("Faltan parametros./ <ID del Usuario> <cantidad a restar>")

    try:
        args[1] = abs(int(args[1]))

    except:
        return await ctx.send("No se puede restar, `{}` no es valido".format(args[1]))

    #print(args[0])
    args[0] = str(args[0]).replace('<@', '').replace('!', '').replace('>', '')
    #print(args[0])

    doc_ref = await get_user_xp(str(ctx.message.guild.id), str(args[0]))
    admin_xp = doc_ref.get()

    if admin_xp.to_dict() is not None and 'exp' in admin_xp.to_dict():
        exp = int(admin_xp.to_dict()['exp']) - args[1]

        confirmation = BotConfirmation(ctx=ctx, color=0x012345)
        await confirmation.confirm("Estas seguro de restar `{}xp` a <@{}>?\n Exp:`{}`".format(args[1], args[0], exp))

        if confirmation.confirmed:
            doc_ref.update({
                'exp': exp
            })
            txt = "Exp restada con exito de <@{}>".format(args[0])
            return await confirmation.update(txt, hide_author=False, color=0x55ff55)
        else:
            return await confirmation.update("Cancelado...", hide_author=False, color=0xff5555)

    else:
        return await ctx.send("No se encontro el usuario")


async def AddExp(ctx):
    args = ctx.message.content.split(" ")[1:]
    if len(args) < 2:
        return await ctx.send("Faltan parametros./ <ID del Usuario> <cantidad a sumar>")

    try:
        args[1] = abs(int(args[1]))

    except:
        return await ctx.send("No se puede sumar, `{}` no es valido".format(args[1]))

    print(args[0])
    args[0] = str(args[0]).replace('<@', '').replace('!', '').replace('>', '')
    print(args[0])

    doc_ref = await get_user_xp(str(ctx.message.guild.id), str(args[0]))
    admin_xp = doc_ref.get()

    if admin_xp.to_dict() is not None and 'exp' in admin_xp.to_dict():
        exp = int(admin_xp.to_dict()['exp']) + args[1]

        confirmation = BotConfirmation(ctx=ctx, color=0x012345)
        await confirmation.confirm("Estas seguro de agregar `{}xp` a <@{}>?\n Exp:`{}`".format(args[1], args[0], exp))

        if confirmation.confirmed:
            doc_ref.update({
                'exp': exp
            })
            txt = "Exp agregada con exito de <@{}>".format(args[0])
            return await confirmation.update(txt, hide_author=False, color=0x55ff55)
        else:
            return await confirmation.update("Cancelado...", hide_author=False, color=0xff5555)


    else:
        return await ctx.send("No se encontro el usuario")


async def ResetExp(ctx):
    doc_ref = db.collection(str(ctx.message.guild.id)).document('Datos').collection('Exp')

    confirmation = BotConfirmation(ctx=ctx, color=0x012345)
    await confirmation.confirm("Estas seguro de reiniciar la xp a todos los usuarios del servidor?")

    if confirmation.confirmed:
        con = await delete_collection(doc_ref, 25)
        txt = "Exp reiniciada con exito de {} usuarios".format(con)
        return await confirmation.update(txt, hide_author=False, color=0x55ff55)

    else:
        return await confirmation.update("Cancelado...", hide_author=False, color=0xff5555)

