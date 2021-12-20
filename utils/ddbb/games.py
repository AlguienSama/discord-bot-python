import time
import discord
from discord.ext.commands import CommandInvokeError
from datetime import datetime, timedelta
from .DB import __get__, __set__
from utils.errors import TimeError, NotMoneyError
from firebase_admin import firestore

db = firestore.client()


async def start_tic_tac_toe(server: int):
    cross = ':x:'
    circle = ':o:'
    try:
        cross = await __get__(str(server), 'games', 'tic_tac_toe', 'pieces', 'cross')
    except:
        pass
    try:
        circle = await __get__(str(server), 'games', 'tic_tac_toe', 'pieces', 'circle')
    except:
        pass

    return cross, circle
