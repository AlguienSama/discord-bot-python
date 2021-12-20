import time
import discord
from discord import User, Guild
from discord.ext.commands import CommandInvokeError
from datetime import datetime, timedelta
from .DB import __get__, __set__, __count__
from utils.errors import TimeError, NotMoneyError
from firebase_admin import firestore

db = firestore.client()

type = 'punishments'


class Punishment:
    def __init__(self, guild_id, user_id, user_name, author_id, author_name, reason, type, time=0):
        self.id = 0
        self.guild_id = str(guild_id)
        self.user_id = str(user_id)
        self.user_name = user_name
        self.author_id = str(author_id)
        self.author_name = author_name
        self.reason = reason
        self.type = type
        self.time = time
        self.date = str(datetime.utcnow())

    async def set_id(self):
        ref = db.collection(str(self.guild_id)).document('Datos').collection(type)\
            .order_by(u'date', direction=firestore.Query.DESCENDING).limit(1).stream()
        doc = list(ref)
        try:
            self.id = int(doc[0].id)+1
        except:
            self.id = 1


async def set_warn(guild: Guild, user: User, author: User, reason: str):
    return await create_punish(guild, user, author, reason, 'warn')


async def set_mute(guild: Guild, user: User, author: User, reason: str, time=0):
    return await create_punish(guild, user, author, reason, 'mute', time)


async def set_kick(guild: Guild, user: User, author: User, reason: str):
    return await create_punish(guild, user, author, reason, 'kick')


async def set_ban(guild: Guild, user: User, author: User, reason: str):
    return await create_punish(guild, user, author, reason, 'ban')


async def set_unban(guild: Guild, user: User, author: User, reason: str):
    return await create_punish(guild, user, author, reason, 'unban')


async def create_punish(guild: Guild, user: User, author: User, reason: str, type: str, time=0):
    punish = Punishment(guild.id, user.id, f'{user.name}#{user.discriminator}',
                        author.id, f'{author.name}#{author.discriminator}', reason, type, time)
    await punish.set_id()
    await __set_punishment(punish)
    return punish.id


async def get_punishment(guild: Guild, id: int):
    return __get__(str(guild.id), type, str(id))


async def get_punishments(guild: Guild, user: User):
    return db.collection(str(guild.id)).document('Datos').collection(type).where(u'user_id', u'==', str(user.id))


async def __set_punishment(punish: Punishment):
    doc = db.collection(str(punish.guild_id)).document('Datos').collection(type).document(str(punish.id))
    return doc.set(punish.__dict__)
