import os
import firebase_admin
import discord
import time, urllib.request
import asyncio

from discord.ext import commands
from dotenv import load_dotenv
from firebase_admin import credentials
from utils.errors import errors

load_dotenv()

# Use a service account
cred = credentials.Certificate(f'./utils/ddbb/keys/{os.getenv("DB_CERTIFICATE")}')
firebase_admin.initialize_app(cred)

description = '''Esto es la descripción para el comando de ayuda predeterminado'''

errores = {
    355104003572498435,  # Ali
    528216772592140290,  # Masc
    226457982773362688,  # Skorpi
    548655370181279749,  # Von
}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=os.getenv('PREFIX'), description=description, owner_ids=errores, case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle)
    # with open('unknown.png', 'rb') as f:
    #    await bot.user.edit(avatar=f.read())
    print(f'Logged in as {bot.user.name}!')


@bot.event
async def on_command_error(ctx, error):
    # print(error.__class__.__name__)
    await errors(ctx, error)


async def load_extensions(dir):
    with os.scandir(dir) as files:
        for file in files:
            if dir != './' and os.path.isfile(os.path.join(dir, file.name)) and file.name.endswith('.py'):
                new_dir = os.path.join(dir, file.name[:-3]).replace('\\', '/')
                new_dir = new_dir.replace('./', '').replace('/', '.')
                # print(new_dir)
                await bot.load_extension(new_dir)

            elif not os.path.isfile(os.path.join(dir, file)):
                try:
                    await load_extensions(os.path.join(dir, file.name).replace('\\', '/'))
                except:
                    pass


async def load_commands():
    await load_extensions('./commands/admin')
    await load_extensions('./commands/economy')
    await load_extensions('./commands/games')
    await load_extensions('./commands/moderation')
    await load_extensions('./commands/music')
    await load_extensions('./commands/reactions')
    await load_extensions('./commands/settings')
    await load_extensions('./commands/together')
    await load_extensions('./commands/utility')
    await load_extensions('./commands/tinder')

asyncio.run(load_commands())

TOKEN = os.getenv('DISCORD_TOKEN')
#bot.run(TOKEN)
has_internet = False

while not has_internet:
    try:
        urllib.request.urlopen('http://google.com')
        has_internet = True
    except:
        has_internet = False

    if not has_internet:
        print('[+] No internet connection, waiting...')
        time.sleep(1.0)
        

bot.run(TOKEN)
