import discord
import json
from utils.ddbb.DB import get_command, get_command_list
from disputils import BotEmbedPaginator, BotConfirmation
from datetime import datetime


async def add_command(ctx, cmd, img, args):
    color = '#000000'
    desc = ''

    if args is not None and len(args) > 0:
        if args[0][0] == '#':
            color = args[0]
            desc = " ".join(args[1:])

        else:
            desc = " ".join(args)

    new_cmd = {
        'id': str(int(datetime.now().strftime('%Y%m%d%H%M%S')[1:])),
        'cmd': cmd,
        'img': img,
        'desc': desc,
        'color': color,
        'user': f'{ctx.author.id} - {ctx.author.name}'
    }

    #print(json.dumps(new_cmd))

    embed = discord.Embed()
    embed.description = str(new_cmd['desc'])
    embed.set_image(url=new_cmd['img'])
    embed.colour = int(str(new_cmd['color']).replace('#', '0x'), 16)

    await ctx.send(content=f'ID: `{new_cmd["id"]}` | comando: `{new_cmd["cmd"]}`', embed=embed)

    confirmation = BotConfirmation(ctx=ctx, color=0x012345)
    await confirmation.confirm("¿Quieres agregar el comando?")

    if confirmation.confirmed:
        doc_ref = await get_command(cmd)
        DocRef = doc_ref.get()

        gifs = []

        if DocRef.to_dict() is not None and ('gifs' in DocRef.to_dict()):
            gifs = DocRef.to_dict()['gifs']
            gifs.append(json.dumps(new_cmd))
            doc_ref.update({
                'gifs': gifs
            })
        else:
            gifs.append(json.dumps(new_cmd))
            doc_ref.set({
                'gifs': gifs
            })

        txt = "Comando agregada con exito"
        return await confirmation.update(txt, hide_author=False, color=0x55ff55)
    else:
        return await confirmation.update("Cancelado...", hide_author=False, color=0xff5555)

async def remove_command(ctx, cmd, id):
    doc_ref = await get_command(cmd)
    DocRef = doc_ref.get()

    if DocRef.to_dict() is not None and ('gifs' in DocRef.to_dict()):
        gifs = DocRef.to_dict()['gifs']
        g = ''
        comando = {}
        sw = False
        for gif in gifs:
            if str(id) in gif:
                g = gif
                comando = json.loads(gif)
                sw = True
                break

        if sw:
            embed = discord.Embed()
            embed.description = str(comando['desc'])
            embed.set_image(url=comando['img'])
            embed.colour = int(str(comando['color']).replace('#', '0x'), 16)

            await ctx.send(content=f'ID: `{comando["id"]}` | comando: `{comando["cmd"]}` | user: {comando["user"]}',
                           embed=embed)

            confirmation = BotConfirmation(ctx=ctx, color=0x012345)
            await confirmation.confirm("¿Quieres eliminar el comando?")

            if confirmation.confirmed:
                gifs.remove(g)
                doc_ref.update({
                    'gifs': gifs
                })
                txt = "Comando eliminado con exito"
                return await confirmation.update(txt, hide_author=False, color=0x55ff55)
            else:
                return await confirmation.update("Cancelado...", hide_author=False, color=0xff5555)

        else:
            return await ctx.send(content=f'El ID: `{id}` no pertenece al comando `{cmd}`')

    else:
        return await ctx.send(content='El comando no existe')

async def lista_comandos(ctx, cmd, id):
    docs = await get_command_list(cmd)

    if cmd is None:
        embed = discord.Embed()
        embed.title = "Lista de comandos"
        Embeds = []
        con = 0
        np = 10
        nom_cmd = ''
        com_cmd = ''

        docs = list(docs)

        for doc in docs:
            if doc.to_dict() is not None and ('gifs' in doc.to_dict()):
                gifs = doc.to_dict()['gifs']
                x = len(gifs)

                con = con + 1

                nom_cmd = nom_cmd+f'> **{doc.id}**\n'
                com_cmd = com_cmd+f'`{x}`\n'

                if con >= np or docs[len(docs)-1] == doc:
                    embed.add_field(name="Comando", value=f'{nom_cmd}')
                    embed.add_field(name="Cantidad", value=f'{com_cmd}')
                    con = 0
                    Embeds.append(embed)
                    embed = discord.Embed()
                    embed.title = "Lista de comandos"
                    embed.description = ''


        paginator = BotEmbedPaginator(ctx, Embeds)
        await paginator.run()

    else:
        if docs.to_dict() is not None and ('gifs' in docs.to_dict()):
            embed = discord.Embed()
            embed.title = f"Lista de comandos \"{cmd}\""
            Embeds = []
            con = 0
            np = 10
            id_cmd = ''
            user_cmd = ''
            img_cmd = ''

            gifs = docs.to_dict()['gifs']

            for gif in gifs:
                comando = json.loads(gif)

                if id is None:
                    con = con + 1

                    id_cmd = id_cmd + f'`#{comando["id"]}`\n'
                    user_cmd = user_cmd + f'<@{comando["user"].split(" ")[0]}>\n'
                    img_cmd = img_cmd + f'[ver]({comando["img"]})\n'

                    if con >= np or gifs[len(gifs) - 1] == gif:
                        embed.add_field(name="ID", value=f'{id_cmd}')
                        embed.add_field(name="User", value=f'{user_cmd}')
                        embed.add_field(name="Imagen", value=f'{img_cmd}')
                        con = 0
                        Embeds.append(embed)
                        embed = discord.Embed()
                        embed.title = f"Lista de comandos \"{cmd}\""

                elif comando["id"] == id:
                    embed = discord.Embed()
                    embed.title = f"Comando \"{cmd}\" `#{id}`"
                    embed.description = \
                    f"""
                    **Usuario:** <@{comando["user"].split(" ")[0]}> `{comando["user"].split(" ")[2]}`
                    **Fecha:** `{id_to_date(comando['id'])}`
                    **Color:** `{comando['color']}`
                    **Imagen:** {comando['img']}
                    
                    **Descripcion:** 
                    {comando['desc']}
                    """
                    embed.set_image(url=comando['img'])
                    embed.colour = int(str(comando['color']).replace('#', '0x'), 16)

                    return await ctx.send(embed=embed)

            if id is None:
                if len(Embeds) == 0:
                    embed.description = 'No hay imagenes para este comando'
                    Embeds.append(embed)

                paginator = BotEmbedPaginator(ctx, Embeds)
                await paginator.run()
            else:
                return await ctx.send(f"No existe el id `{id}` en el comando \"{cmd}\"")

        else:
            return await ctx.send(f"El comando \"{cmd}\" no existe")


def id_to_date(id):
    y = f"20{id[:2]}"
    m = id[2:4]
    d = id[4:6]
    hh = id[6:8]
    mm = id[8:10]
    ss = id[10:12]

    return f"{d}/{m}/{y} {hh}:{mm}:{ss}"
