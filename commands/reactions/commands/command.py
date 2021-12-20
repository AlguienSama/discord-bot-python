import discord
import json

from firebase_admin import firestore
from discord.ext.commands import Bot, Context
from discord_slash import SlashContext
from random import choice
from utils.ddbb.DB import get_command


db = firestore.client()


async def Command(message, nombre):
    content = " ".join(message.content.split(" ")[1:])

    doc_ref = await get_command(nombre)
    DocRef = doc_ref.get()

    if DocRef.to_dict() is not None and ('gifs' in DocRef.to_dict()):
        jsons = DocRef.to_dict()['gifs']
        gif = json.loads(choice(jsons))

        embed = discord.Embed()
        embed.description = str(gif['desc']).replace('%user%', str(message.author.mention)).replace('%target%', str(content))
        embed.set_image(url=gif['img'])
        embed.colour = int(str(gif['color']).replace('#', '0x'), 16)

        return await message.channel.send(embed=embed)

    return
