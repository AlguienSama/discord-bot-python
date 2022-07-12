import discord
from discord import User
from discord.ext.commands import *
from utils.ddbb.tinder import *
from utils.responses.Embed import Embed
from utils.errors import CustomError


def build_profile(user) -> discord.Embed:
    embed = Embed()
    if "name" in user:
        embed.title = user["name"]
    if "gender" in user:
        if embed.title is None:
            embed.title = f'[{user["gender"]}]'
        else:
            embed.title += f' [{user["gender"]}]'
    if "image" in user:
        embed.set_image(user["image"])
    if "description" in user:
        embed.description = user["description"]
    if "hobbies" in user:
        embed.add_field('Hobbies', user["hobbies"])
    if "color" in user:
        try:
            color = user["color"].split('#')
            color = color[1] if color[1] is not None else color[0]
            embed.color = int('0x'+color, base=16)
        except:
            embed.color = int(user["color"])
    if "phrase" in user:
        embed.set_author(user["phrase"], "")
    return embed.get_embed()


class PersistentView(discord.ui.View):
    def __init__(self, bot, user, users: list, author: discord.User):
        super().__init__(timeout=20.0)
        self.author = author
        self.bot = bot
        self.user = user
        self.users = users
        self.index = 0
        self.get_curr_user()
    
    async def on_timeout(self) -> None:
        await self.author.send('**!!Tiempo finalizado, vuelve a usar otra vez el comando!!**')
        return await super().on_timeout()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception, item) -> None:
        print('Error:', error)
        self.stop()
        return await super().on_error(interaction, error, item)
        
    """ @discord.ui.button(label='Atrás', emoji='\U00002B05', style=discord.ButtonStyle.grey, custom_id='persistent_view:grey')
    async def grey(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index == 0:
            return await interaction.response.send_message('No usuarios para mostrar hacia atrás.', ephemeral=True)
        
        self.index-=1
        await self.update_embed(interaction) """

    @discord.ui.button(label='Rechazar', emoji='\U00002716', style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await tinder_reject(self.user["id"], self.curr_user_id)
        await self.next_page(interaction)
        
    @discord.ui.button(label='Like', emoji='\U00002705', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await tinder_like(self.user["id"], self.curr_user_id)
        await self.check_match()
        await self.next_page(interaction)
        
    async def check_match(self):
        if "liked" in self.curr_user and str(self.user["id"]) in self.curr_user["liked"]:
            try:
                user: discord.User = await self.bot.fetch_user(self.curr_user_id)
                await user.send('**!!Nuevo match!!**')
                await user.send(f'{self.author}')
                await self.author.send('**!!Nuevo match!!**')
                await self.author.send(content=f'{user}')
                await tinder_match(self.user["id"], self.curr_user_id)
            except:
                pass

    def get_curr_user(self):
        curr_user = self.users[self.index]
        self.curr_user_id = list(curr_user.keys())[0]
        self.curr_user = curr_user[self.curr_user_id]

    async def next_page(self, interaction: discord.Interaction):
        self.index+=1
        if self.index == len(self.users):
            self.index-=1
            await interaction.response.edit_message(view=self, embed=discord.Embed(title="No hay más usuarios para mostrar"))
            return self.stop()
        await self.update_embed(interaction)
    
    async def update_embed(self, interaction: discord.Interaction):
        self.get_curr_user()
        await interaction.response.edit_message(view=self, embed=build_profile(self.curr_user))


class Tinder(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    
    async def __get_user_data(self, user_id):
        doc_ref = await tinder_get_user(user_id)
        user_data = doc_ref.get()
        return user_data.to_dict()
    
    
    async def __get_reminding_options(self, user: User):
        msg = ""
        user_data = await self.__get_user_data(user.id)
        
        def has_property(property, text):
            try:
                if user_data[property] is None:
                    return "" + text + "\n"
                return ""
            except:
                return "" + text + "\n"
        
        msg += has_property("name", "`*tnombre tu nombre`")
        msg += has_property("gender", "`*tgenero masculino / femenino / ...`")
        msg += has_property("image", "`*timagen url de la imagen`")
        msg += has_property("description", "`*tdesc una descripción sobre ti`")
        msg += has_property("hobbies", "`*thobbies tus hobbies`")
        msg += has_property("phrase", "`*tfrase una frase para conquistar`")
        msg += has_property("color", "`*tcolor color hex para poner en el embed (ej: #00f0ff)`")
        if msg != "":
            await user.send(msg)
    
    
    @command(name='tnombre')
    async def _tinder_name(self, ctx: Context, *, name: str):
        """<nombre>"""
        await tinder_set_name(ctx.author.id, name)
        await self._tinder_profile(ctx)
    
    @command(name='tgenero')
    async def _tinder_gender(self, ctx: Context, *, gender: str):
        """<género femenino / masculino / ...>"""
        await tinder_set_gender(ctx.author.id, gender)
        await self._tinder_profile(ctx)
    
    @command(name='timagen')
    async def _tinder_image(self, ctx: Context, image: str):
        """<url imagen>"""
        await tinder_set_image(ctx.author.id, image)
        await self._tinder_profile(ctx)
    
    @command(name='tdesc')
    async def _tinder_description(self, ctx: Context, *, description: str):
        """<descripción>"""
        await tinder_set_description(ctx.author.id, description)
        await self._tinder_profile(ctx)
    
    @command(name='thobbies')
    async def _tinder_hobbies(self, ctx: Context, *, hobbies: str):
        """<lista de hobbies>"""
        await tinder_set_hobbies(ctx.author.id, hobbies)
        await self._tinder_profile(ctx)
        
    @command(name='tfrase')
    async def _tinder_phrase(self, ctx: Context, *, phrase: str):
        """<frase para conquistar a la gente o no se, ilústrense>"""
        await tinder_set_phrase(ctx.author.id, phrase)
        await self._tinder_profile(ctx)
        
    @command(name='tcolor')
    async def _tinder_color(self, ctx: Context, color: str):
        """<color en hexadecimal (ej: #00f0ff)>"""
        try:
            color = color.split('#')
            color = color[0] if len(color) == 1 else color[1]
            color = int('0x'+color, 16)
        except:
            raise CustomError("Color inválido")
        
        await tinder_set_color(ctx.author.id, color)
        await self._tinder_profile(ctx)
    
    @command(name='tperfil')
    async def _tinder_profile(self, ctx: Context):
        """Ver tu perfil"""
        try:
            user = await self.__get_user_data(ctx.author.id)
            embed = build_profile(user)
            await self.__get_reminding_options(ctx.author)
            await ctx.author.send(embed=embed)
        except Exception as e:
            print(e)
            raise CustomError("No tienes un perfil creado `*help Tinder`")
    
    @command(name="tinder")
    async def _tinder(self, ctx: Context):
        """"""        
        user = await self.__get_user_data(ctx.author.id)
        try:
            user["id"] = ctx.author.id
        except:
            raise CustomError("No tienes un perfil creado `*help Tinder`")
        users_list = (await tinder_get_list()).stream()
        users = []
        for _user in users_list:
            if int(_user.id) != user["id"] and not \
                ("liked" in user and str(_user.id) in user["liked"]) and not \
                ("rejected" in user and str(_user.id) in user["rejected"]) and not \
                ("matched" in user and str(_user.id) in user["matched"]):
                    users.append({_user.id: _user.to_dict()})
    
        if len(users) == 0:
            raise CustomError("No hay nadie más para ver")
        
        curr_user = users[0]
        curr_user_id = list(curr_user.keys())[0]
        await ctx.author.send(embed=build_profile(curr_user[curr_user_id]), view=PersistentView(self.bot, user, users, ctx.author))
        #['⬅', '❌', '✅']
        #reactions = [u'\U00002B05', u'\U0000274C', u'\U00002705']


async def setup(bot: Bot) -> None:
    await bot.add_cog(Tinder(bot))
