import time
import discord
from discord.ext.commands import CommandInvokeError
from datetime import datetime, timedelta
from .DB import __get__, __set__
from utils.errors import TimeError, NotMoneyError
from firebase_admin import firestore

db = firestore.client()


async def get_bal(server: int, user: int):
    return await __get__(str(server), 'economy', str(user))


async def set_bal(server: int, user: int, money: int = 0):
    return await __set__(str(server), 'economy', str(user), {
        "money": money,
        "inventory": []
    })


async def update_bal(server: int, user: int, money: int):
    doc = await get_bal(server, user)
    try:
        doc.update({'money': firestore.Increment(money)})
    except:
        return await set_bal(server, user, money)

    return doc


async def check_bal(server: int, user: int, money: int):
    bal = await get_bal(server, user)
    bal = bal.get()
    bal = bal.to_dict()
    if bal is None:
        raise NotMoneyError(money)

    if bal["money"] < money:
        raise NotMoneyError((bal["money"] - money) * -1)


def work_time() -> datetime:
    return datetime.utcnow() + timedelta(hours=4)


async def update_work(server: int, user: int, money: int):
    global time
    doc = await get_bal(server, user)
    try:
        time = doc.get()
        time = datetime.strptime(time.to_dict()['work_time'], '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(e)
        return await __set__(str(server), 'economy', str(user), {
            "money": money,
            "inventory": [],
            "work_time": work_time().strftime('%Y-%m-%d %H:%M:%S')
        })

    act_time = datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    if time > act_time:
        raise TimeError(time - act_time)
    doc.update({'money': firestore.Increment(money), "work_time": work_time().strftime('%Y-%m-%d %H:%M:%S')})

    return doc


async def get_items(server: int, category=None):
    doc_ref = db.collection(str(server)).document('Datos').collection('shop')
    if category is not None:
        doc_ref.where(u'category', u'==', category.lower())

    
