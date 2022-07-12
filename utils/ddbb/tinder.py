from firebase_admin import firestore

db = firestore.client()

async def tinder_get_user(user_id: int):
    return db.collection('tinder').document(str(user_id))

async def tinder_get_list():
    return db.collection('tinder')

async def tinder_set(user_id: int, data: object):
    doc = await tinder_get_user(user_id)
    try:
        return doc.update(data)
    except:
        return doc.set(data)

async def tinder_set_name(user_id: int, name: str):
    return await tinder_set(user_id, {"name": name})

async def tinder_set_image(user_id: int, image: str):
    return await tinder_set(user_id, {"image": image})

async def tinder_set_gender(user_id: int, gender: str):
    return await tinder_set(user_id, {"gender": gender})

async def tinder_set_description(user_id: int, description: str):
    return await tinder_set(user_id, {"description": description})

async def tinder_set_hobbies(user_id: int, hobbies: str):
    return await tinder_set(user_id, {"hobbies": hobbies})

async def tinder_set_phrase(user_id: int, phrase: str):
    return await tinder_set(user_id, {"phrase": phrase})

async def tinder_set_color(user_id: int, color: str):
    return await tinder_set(user_id, {"color": color})

async def tinder_like(user_id: int, user_id_liked: int):
    try:
        return (await tinder_get_user(user_id)).update({"liked": firestore.ArrayUnion([int(user_id_liked)])})
    except Exception as e:
        print(e)
        return await tinder_set(user_id, {"liked": [int(user_id_liked)]})

async def tinder_reject(user_id: int, user_id_rejected: int):
    try:
        return (await tinder_get_user(user_id)).update({"rejected": firestore.ArrayUnion([int(user_id_rejected)])})
    except:
        return await tinder_set(user_id, {"rejected": [int(user_id_rejected)]})

async def tinder_match(user_id: int, user_id_matched: int):
    try:
        (await tinder_get_user(user_id)).update({"matched": firestore.ArrayUnion([int(user_id_matched)])})
    except:
        await tinder_set(user_id, {"matched": [int(user_id_matched)]})
    
    try:
        (await tinder_get_user(user_id_matched)).update({"matched": firestore.ArrayUnion([int(user_id)])})
    except:
        await tinder_set(user_id_matched, {"matched": [int(user_id)]})
        
