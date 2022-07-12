import discord
import requests
import os
import json

from dotenv import load_dotenv
from discord.ext.commands import Bot, Cog, Context, command


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
IDAPP = os.getenv('ID_APP')
auth = "Bot " + TOKEN


class SlashBot(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='slash', aliases=['s'])
    async def slash(self, ctx: Context):
        """activa o desactiva slash del bot en el servidor | slash <enable, true, e> o slash <disable, false, d>"""

        args = ctx.message.content.split(" ")[1:]

        if len(args) < 1:
            return await ctx.send("Faltan parametros")

        elif (args[0].lower() != "enable" and args[0].lower() != "true" and args[0].lower() != "e" and
              args[0].lower() != "disable" and args[0].lower() != "false" and args[0].lower() != "d"):
            return await ctx.send("Parametros Invalido")

        url = "https://discord.com/api/v8/applications/"+str(IDAPP)+"/commands"

        # For authorization, you can use either your bot token
        headers = {
            "Authorization": auth
        }

        if args[0].lower() == "enable" or args[0].lower() == "true" or args[0].lower() == "e":
            pass

        elif args[0].lower() == "disable" or args[0].lower() == "false" or args[0].lower() == "d":
            r = requests.get(url, headers=headers)
            print(r.json())
            for sh in r.json():
                res = requests.delete(url + "/" + str(sh['id']), headers=headers)
                print(res)

            await ctx.send("slash")


async def setup(bot: Bot) -> None:
    await bot.add_cog(SlashBot(bot))
