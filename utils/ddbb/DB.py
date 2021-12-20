import random
import time
import discord

from datetime import datetime
from firebase_admin import firestore

from utils.errors import CustomError

db = firestore.client()


async def __get__(server: str, type: str, query: str):
    return db.collection(server).document('Datos').collection(type).document(query)


async def __count__(server: str, type: str):
    return len(await db.collection(server).document('Datos').collection(type))


async def __get_settings__(server: str, type: str, query: str):
    return db.collection(server).document('Settings').collection(type).document(query)


async def __set__(server: str, type: str, query: str, args: object):
    q = await __get__(server, type, query)
    q.set(args)
    return q


async def __set_settings__(server: str, type: str, query: str, args: object):
    q = await __get_settings__(server, type, query)
    q.set(args)
    return q


async def get_admin_channels(server: str):
    return await __get__(server, 'admin', 'channels')


async def get_admin_xp(server: str):
    return await __get__(server, 'admin', 'exp')


async def get_user_xp(server: str, user: str):
    return await __get__(server, 'Exp', user)


async def top_xp(server):
    ref = db.collection(str(server)).document('Datos').collection('Exp')
    ref = ref.order_by('exp', direction=firestore.Query.DESCENDING).limit(10)
    return ref.stream()


async def get_command(command: str):
    q = db.collection('BOT').document('Datos').collection('comandos').document(command)
    return q


async def get_command_by_id(command: str, id: str):
    return db.collection('BOT').document('commands').collection(command).document(id)


async def get_command_list(cmd):
    if cmd is None:
        q = db.collection('BOT').document('Datos').collection('comandos').stream()
        return q

    else:
        q = db.collection('BOT').document('Datos').collection('comandos').document(cmd).get()
        return q


async def set_command(command: str, img: str, user: discord.User, color: int = 0, text: str = None):
    rand_id = str(int(datetime.now().strftime('%Y%m%d%H%M%S')[1:]))
    q = db.collection('BOT').document('Datos').collection('comandos').document(command)
    q.set({"img": img, "user": f'{user.id} - {user.name}', "color": color, "text": text})
    return await get_command_by_id(command, id=rand_id)


async def set_enabled_commands(server: int, command: str, channels: [int]):
    q = await __get_settings__(str(server), 'commands', command)
    if q.get().to_dict() is None:
        return await __set_settings__(str(server), 'commands', command, {'channels': channels})

    return q.update({'channels': firestore.firestore.ArrayUnion(channels)})


async def set_disabled_commands(server: int, command: str, channels: [int]):
    q = await __get_settings__(str(server), 'commands', command)

    if q is None:
        raise CustomError('No hay canales para deshabilitar para este comando')

    return q.update({'channels': firestore.firestore.ArrayRemove(channels)})


async def get_disabled_command(server: int, command: str):
    return await __get_settings__(str(server), 'commands', command)


async def delete_collection(coll_ref, batch_size, con=None):
    if con is None:
        con = 0

    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1
        con = con + 1

    if deleted >= batch_size:
        return await delete_collection(coll_ref, batch_size, con)

    else:
        return con
