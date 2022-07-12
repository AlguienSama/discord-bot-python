import datetime

from firebase_admin import firestore
from discord.ext.commands import Bot, Context
from discord import User
from utils.responses.Embed import Embed
from utils.ddbb.DB import get_admin_xp, get_user_xp, top_xp

db = firestore.client()


async def experiencia(message):
    t = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)

    doc_ref = None
    try: 
        doc_ref = await get_user_xp(str(message.guild.id), str(message.author.id))
    except:
        return
    
    user_xp = doc_ref.get()

    xp = 5
    sw = True
    user_xp = user_xp.to_dict()
    meta = 0

    # Aumentamos la xp
    if user_xp is not None:
        xp = user_xp['exp'] + 5
        time = datetime.datetime.strptime(user_xp['time'], '%Y-%m-%d %H:%M:%S.%f')
        if 'meta' in user_xp:
            meta = user_xp['meta']
        # Si no sube la xp, termina
        if time > datetime.datetime.utcnow():
            return

    if sw:
        doc_ref.set({
            "exp": xp,
            "time": str(t),
            "meta": int(meta)
        })

    user_xp = xp
    user_meta = meta

    doc_metas = await get_admin_xp(str(message.guild.id))
    admin_xp = doc_metas.get()
    admin_xp = admin_xp.to_dict()

    if admin_xp is not None and ('metas' in admin_xp):
        metas = admin_xp['metas']
        
        current_meta = None
        for meta in metas:
            # Getting user meta
            if user_meta == meta['id']:
                user_meta = meta
            if user_xp > meta['exp'] and current_meta is None:
                current_meta = meta
            elif user_xp > meta['exp'] and current_meta is not None and current_meta['exp'] < meta['exp']:
                current_meta = meta

        try:
            if (user_meta == 0 and current_meta is not None) or (not 'id' in user_meta and current_meta is not None and ('id' in current_meta and (user_meta['id'] != current_meta['id'])) and not 'id' in current_meta):
                # Update ddbb
                doc_ref.update({'meta': int(current_meta['id'])})
                # Update user roles
                if user_meta != 0 and 'id' in user_meta:
                    await message.author.remove_roles(message.guild.get_role(int(user_meta['rol'])))
                await message.author.add_roles(message.guild.get_role(int(current_meta['rol'])))
                    

                # Send msg
                msg = current_meta['msg'] if 'msg' in current_meta else "Nueva meta alcanzada"
                msg = msg.replace('%user%', '<@' + str(message.author.id) + '>')
                if 'canal' in admin_xp:
                    canal = admin_xp['canal']
                    if canal == 'dm':
                        await message.author.send(msg)
                    elif canal == 'normal':
                        await message.channel.send(msg)
                    elif canal == 'none':
                        return
                    else:
                        idcanal = int(canal)
                        await message.guild.get_channel(idcanal).send(msg)
                else:
                    await message.channel.send(msg)
                
                # Log message
                await message.guild.get_channel(945371397847404554).send(msg)
        except:
            pass


async def getExp(ctx):
    # TODO: Try catch with errors

    args = ctx.message.content.split(" ")[1:]

    id_User = ctx.message.author.id

    if len(args) > 0:
        id_User = str(args[0]).replace('<@', '').replace('!', '').replace('>', '')

    doc_ref = await get_user_xp(str(ctx.message.guild.id), str(id_User))
    user_xp = doc_ref.get()

    xp = 0

    if user_xp.to_dict() is not None and ('exp' in user_xp.to_dict()):
        xp = user_xp.to_dict()['exp']

    usuario = await ctx.guild.fetch_member(int(id_User))

    embed = Embed(user=usuario, title="Experiencia: {}".format(usuario),
                  description="Exp: {}".format(xp)).success().get_embed()

    # si el comando se llama normalmente
    if type(ctx) == Context:
        return await ctx.send(embed=embed)


async def rank_xp(bot: Bot, ctx: Context):
    top = await top_xp(ctx.guild.id)
    embed = Embed(title='Ranking Server XP').success()
    for i, doc in enumerate(top):
        user: User = await bot.fetch_user(int(doc.id))
        embed.add_field(f'#{i+1} {user.name}#{user.discriminator}', f'Nivel X - {doc.to_dict()["exp"]}xp')

    return await ctx.send(embed=embed.get_embed())
