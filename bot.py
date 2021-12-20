import os
import firebase_admin
import discord

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
}
bot = commands.Bot(command_prefix=os.getenv('PREFIX'), description=description, owner_ids=errores,
                   case_insensitive=True)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle)
    # with open('unknown.png', 'rb') as f:
    #    await bot.user.edit(avatar=f.read())
    print('Logged in as @' + bot.user.name + '#' + bot.user.discriminator)


@bot.event
async def on_command_error(ctx, error):
    # print(error.__class__.__name__)
    await errors(ctx, error)


def load_extensions(dir):
    with os.scandir(dir) as files:
        for file in files:
            if dir != './' and os.path.isfile(os.path.join(dir, file.name)) and file.name.endswith('.py'):
                new_dir = os.path.join(dir, file.name[:-3]).replace('\\', '/')
                new_dir = new_dir.replace('./', '').replace('/', '.')
                # print(new_dir)
                bot.load_extension(new_dir)

            elif not os.path.isfile(os.path.join(dir, file)):
                try:
                    load_extensions(os.path.join(dir, file.name).replace('\\', '/'))
                except:
                    pass


load_extensions('./commands/admin')
load_extensions('./commands/economy')
load_extensions('./commands/games')
load_extensions('./commands/moderation')
load_extensions('./commands/music')
load_extensions('./commands/reactions')
load_extensions('./commands/settings')
load_extensions('./commands/together')
load_extensions('./commands/utility')

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
