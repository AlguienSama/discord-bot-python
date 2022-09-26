from datetime import datetime

from .DB import __get_game__, __set_game__, __get__
from utils.errors import CustomError
from firebase_admin import firestore

db = firestore.client()

async def oj_get_card(server: int, user: int):
    try:
        return db.collection(str(server)).document('games').collection('oj').document(str(user)).get().to_dict()
    except Exception as e:
        print('error oj_get_card', e)
        return None

async def oj_set_card(server: int, user: int, data: object):
    try:
        await __set_game__(str(server), 'oj', str(user), data)
    except Exception as e:
        print('error oj_set_card', e)

async def start_tic_tac_toe(server: int):
    cross = ':x:'
    circle = ':o:'
    try:
        cross = await __get_game__(str(server), 'tic_tac_toe', 'pieces', 'cross')
    except:
        pass
    try:
        circle = await __get_game__(str(server), 'tic_tac_toe', 'pieces', 'circle')
    except:
        pass

    return cross, circle

async def br_save_player(server: int, player):
    try:
        id = 1
        ref = db.collection(str(server)).document('games').collection('br')\
            .order_by(u'date', direction=firestore.Query.DESCENDING).limit(1).stream()
        doc = list(ref)
        try:
            id = int(doc[0].id)+1
            if id > 32:
                CustomError("Máximo de jugadores alcanzados")
        except:
            pass
        await __set_game__(str(server), 'br', str(id), {'id': player.id, 'name': player.name, 'image': player.image, 'date': datetime.now()})
    except Exception as e:
        print('error save player br')
        print(e)
        pass

async def br_get_players(server: int):
    try:
        db.collection(server).document('games').collection('br')
    except:
        pass
