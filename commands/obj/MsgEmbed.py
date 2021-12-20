import discord
import json


class MsgEmbed:
    def __init__(self, valor, n: None):
        self.msg = None
        self.content = None
        self.tts = None
        self.embed = None
        #print(valor)
        try:
            if valor.startswith("{") and valor.endswith("}"):
                self.msg = json.loads(valor)
                # print(self.msg)
                if "plainText" in self.msg:
                    self.content = self.msg["plainText"]

                if "tts" in self.msg:
                    self.tts = self.msg["tts"]

                self.embed = self.toEmbed(msg=self.msg)

            else:
                self.content = valor

        except:
            self.content = "***... ERROR ...***" + " `id: {0}`".format(n) if n is not None else ""

        #print(self.content)
        #print(self.tts)
        #print(self.embed)

    def toEmbed(self, msg: dict):
        embed = discord.Embed()
        embed.title = msg["title"] if "title" in msg else ""
        embed.description = msg["description"] if "description" in msg else ""
        embed.url = msg["url"] if "url" in msg else ""

        if "author" in msg:
            nombre = msg["author"]["name"] if "name" in msg["author"] else ""
            url = msg["author"]["url"] if "url" in msg["author"] else ""
            icono = msg["author"]["icon_url"] if "icon_url" in msg["author"] else ""
            embed.set_author(name=nombre, url=url, icon_url=icono)

        if "color" in msg:
            embed.colour = int(msg["color"].replace("#", "0x"), 16)

        if "footer" in msg:
            txt = msg["footer"]["text"] if "text" in msg["footer"] else ""
            url = msg["footer"]["icon_url"] if "icon_url" in msg["footer"] else ""
            embed.set_footer(text=txt, icon_url=url)

        embed.set_thumbnail(url=(msg["thumbnail"] if "thumbnail" in msg else ""))
        embed.set_image(url=(msg["image"] if "image" in msg else ""))

        if "fields" in msg:
            for f in msg["fields"]:
                embed.add_field(name=f["name"], value=f["value"], inline=(f["inline"] if "inline" in f else False))

        return embed
