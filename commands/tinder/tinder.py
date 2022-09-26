import asyncio
import discord
from discord import User
from discord.ext.commands import *
from utils.ddbb.tinder import *
from utils.responses.Embed import Embed
from utils.errors import CustomError


class Profile():
    def __init__(self, user: User):
        self.user = user
        self.name = None
        self.gender = None
        self.sex_preference = None
        self.age = None
        self.image = None
        self.description = None
        self.hobbies = None
        self.color = '#ffffff'

    async def get_user_data(self):
        doc_ref = await tinder_get_user(self.user.id)
        user_data = doc_ref.get()
        if user_data is not None:
            user_data = user_data.to_dict()
            self.age = user_data['age'] if 'age' in user_data else None
            self.color = user_data['color'] if 'color' in user_data else '#bf4035'
            self.description = user_data['description'] if 'description' in user_data else None
            self.gender = user_data['gender'] if 'gender' in user_data else None
            self.hobbies = user_data['hobbies'] if 'hobbies' in user_data else None
            self.image = user_data['image'] if 'image' in user_data else None
            self.name = user_data['name'] if 'name' in user_data else None
            self.sex_preference = user_data['sex_preference'] if 'sex_preference' in user_data else None
        return self
            
    async def save(self):
        await tinder_set(self.user.id, {'age': self.age, 'color': self.color, 'description': self.description, 'gender': self.gender, 'hobbies': self.hobbies, 'image': self.image, 'name': self.name, 'sex_preference': self.sex_preference})
        pass


def build_profile(user: Profile) -> discord.Embed:
    embed = Embed()
    embed.title = user.name
    if embed.title is None:
        embed.title = f'[{user.gender}]'
    else:
        embed.title += f' [{user.gender}]'
    embed.set_image(user.image)
    embed.description = user.description
    embed.add_field('Hobbies', user.hobbies)
    try:
        color = user.color.split('#')
        color = color[1] if color[1] is not None else color[0]
        embed.color = int('0x'+color, base=16)
    except:
            embed.color = int(user.color)
    return embed.get_embed()


class TinderModal(discord.ui.Modal):
    def __init__(self, profile: Profile):
        super().__init__(title="Tinder")
        self.profile = profile
        self.age = discord.ui.TextInput(label="Edad (número)", style=discord.TextStyle.short, placeholder="Edad", required=True, min_length=1, max_length=2, default='' if not hasattr(profile, 'age') else profile.age)
        self.description = discord.ui.TextInput(label="Descripción", style=discord.TextStyle.long, placeholder="Descripción", required=False, default='' if not hasattr(profile, 'description') else profile.description)
        self.gender = discord.ui.Select(placeholder="Género", options=[
            discord.SelectOption(label='Hombre', value='Hombre', default=True if profile.gender == 'Hombre' else False),
            discord.SelectOption(label='Mujer', value='Mujer', default=True if profile.gender == 'Mujer' else False),
            discord.SelectOption(label='Otro', value='Otro', default=True if profile.gender == 'Otro' else False)
        ], min_values=1, max_values=1)
        self.name = discord.ui.TextInput(label="Nombre", style=discord.TextStyle.short, placeholder="Nombre", min_length=1, max_length=50, required=True, default='' if not hasattr(profile, 'name') else profile.name)
        self.sex_preference = discord.ui.Select(placeholder="Que buscas?", options=[
            discord.SelectOption(label='Hombres', value='Hombre', default=True if profile.gender == 'Hombre' else False),
            discord.SelectOption(label='Mujeres', value='Mujer', default=True if profile.gender == 'Mujer' else False),
            discord.SelectOption(label='Todo', value='Otro', default=True if profile.gender == 'Otro' else False)
        ], min_values=1, max_values=1)
        self.add_item(self.name)
        self.add_item(self.age)
        self.add_item(self.gender)
        self.add_item(self.sex_preference)
        self.add_item(self.description)
        
    async def on_submit(self, interaction: discord.Interaction):
        self.profile.name = self.name.value
        age = int(self.age.value)
        if age < 9 or age > 99:
            self.age.value = '-'
        else:
            self.profile.age = age
        self.profile.gender = self.gender.values[0]
        self.profile.sex_preference = self.sex_preference.values[0]
        self.profile.description = self.description.value
        await self.profile.save()
        self.stop()
    

class TinderView(discord.ui.View):
    def __init__(self, bot: Bot, user: User):
        super().__init__(timeout=180)
        self.bot = bot
        self.user = user
    
    @discord.ui.button(label="Editar Perfil", style=discord.ButtonStyle.primary)
    async def profile(self, interaction: discord.Interaction, button):
        user = await (Profile(interaction.user)).get_user_data()
        modal = TinderModal(user)
        try:
            await interaction.response.send_modal(modal)
            timeout = await modal.wait()
            if timeout:
                await interaction.response.send_message("Has cancelado la edición")
            else:
                await interaction.response.send_message(embed=build_profile(user), view=TinderView(self.bot))
        except Exception as e:
            print('Error: '+str(e))
    
    @discord.ui.button(label="Imágen", style=discord.ButtonStyle.primary)
    async def edit_image(self, interaction: discord.Interaction, button):
        class ImageSaveView(discord.ui.View):
            def __init__(self, profile: Profile):
                super().__init__(timeout=60)
                self.cont = True
                self.profile = profile
            
            @discord.ui.button(label="Guardar", style=discord.ButtonStyle.success)
            async def save(self, interaction: discord.Interaction, button):
                self.cont = False
                await self.profile.save()
                await interaction.response.send_message("Imagen guardada correctamente!", ephemeral=True)
                self.stop()
            @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.danger)
            async def cancel(self, interaction: discord.Interaction, button):
                self.cont = False
                await interaction.response.send_message("Has cancelado la edición", ephemeral=True)
                self.stop()
        
        profile = await (Profile(interaction.user)).get_user_data()
        image_view = ImageSaveView(profile)
        msg = await self.user.send("Envía la url de la imagen que quieras usar", embed=build_profile(profile), view=image_view)
        await interaction.response.send_message("Es recomendable usar un enlace terminado con .png o .jpg", ephemeral=True)
        while image_view.cont:
            img: discord.Message = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
            profile.image = img.content
            await img.delete()
            await msg.edit(embed=build_profile(profile))
    
    @discord.ui.button(label="Color", style=discord.ButtonStyle.primary)
    async def edit_color(self, interaction: discord.Interaction, button):
        # mostrar vista de perfil con botón de guardar / cancelar
        # listado de botónes con diferentes colores + opción de añadir uno custom
        class ColorSelectView(discord.ui.View):
            def __init__(self, profile: Profile):
                super().__init__(timeout=60)
                self.cont = True
                self.profile = profile
                self.msg = None
            @discord.ui.button(label="Negro", style=discord.ButtonStyle.gray, emoji='<:000000:1009570113604833402>')
            async def black(self, interaction: discord.Interaction, button):
                self.profile.color = '#000000'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Discord", style=discord.ButtonStyle.gray, emoji='<:2f3136:1009570127924170852>')
            async def dis(self, interaction: discord.Interaction, button):
                self.profile.color = '#2f3136'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Gris", style=discord.ButtonStyle.gray, emoji='<:818181:1009570201509056573>')
            async def gray(self, interaction: discord.Interaction, button):
                self.profile.color = '#818181'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Blanco", style=discord.ButtonStyle.gray, emoji='<:ffffff:1009570267695153194>')
            async def white(self, interaction: discord.Interaction, button):
                self.profile.color = '#ffffff'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Azul", style=discord.ButtonStyle.gray, emoji='<:2246cc:1009570180034220162>')
            async def blue(self, interaction: discord.Interaction, button):
                self.profile.color = '#2246cc'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Cian", style=discord.ButtonStyle.gray, emoji='<:3fbcef:1009570138183442593>')
            async def cyan(self, interaction: discord.Interaction, button):
                self.profile.color = '#3fbcef'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Morado", style=discord.ButtonStyle.gray, emoji='<:67087b:1009570189697892513>')
            async def purple(self, interaction: discord.Interaction, button):
                self.profile.color = '#67087b'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Fucsia", style=discord.ButtonStyle.gray, emoji='<:e3007b:1009570234119749702>')
            async def fuchsia(self, interaction: discord.Interaction, button):
                self.profile.color = '#e3007b'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Rosa", style=discord.ButtonStyle.gray, emoji='<:f59fbc:1009570257972777041>')
            async def pink(self, interaction: discord.Interaction, button):
                self.profile.color = '#f59fbc'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Rojo", style=discord.ButtonStyle.gray, emoji='<:cc2222:1009570211957055601>')
            async def red(self, interaction: discord.Interaction, button):
                self.profile.color = '#cc2222'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Naranja", style=discord.ButtonStyle.gray, emoji='<:e87b1b:1009570222589607986>')
            async def orange(self, interaction: discord.Interaction, button):
                self.profile.color = '#e87b1b'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Amarillo", style=discord.ButtonStyle.gray, emoji='<:f8f400:1009570244936880168>')
            async def yellow(self, interaction: discord.Interaction, button):
                self.profile.color = '#f8f400'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Verde", style=discord.ButtonStyle.gray, emoji='<:006a25:1009570147368976444>')
            async def green(self, interaction: discord.Interaction, button):
                self.profile.color = '#006a25'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Verde Claro", style=discord.ButtonStyle.gray, emoji='<:7cc623:1009570167933632612>')
            async def light_green(self, interaction: discord.Interaction, button):
                self.profile.color = '#000000'
                await interaction.response.edit_message(embed=build_profile(self.profile), view=color_select)
            @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.danger)
            async def cancel(self, interaction: discord.Interaction, button):
                self.cont = False
                await interaction.response.send_message("Has cancelado la edición", ephemeral=True)
                self.stop()
            @discord.ui.button(label="Guardar", style=discord.ButtonStyle.success)
            async def save(self, interaction: discord.Interaction, button):
                self.cont = False
                await self.profile.save()
                await interaction.response.send_message("Imagen guardada correctamente!", ephemeral=True)
                self.stop()
                
        profile = await (Profile(interaction.user)).get_user_data()
        color_select = ColorSelectView(profile)
        msg = await self.user.send("Elige el color que deseas usar", embed=build_profile(profile), view=color_select)
        await interaction.response.send_message("Puedes poner el color enviando el código en formato hexadecimal (ej: `#ff00ff`)", ephemeral=True)
        while color_select.cont:
            color: discord.Message = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
            profile.color = color.content
            await color.delete()
            await msg.edit(embed=build_profile(profile))

    @discord.ui.button(label="Hobbies", style=discord.ButtonStyle.primary)
    async def edit_hobbies(self, interaction: discord.Interaction, button):
        # select con un listado de hobbies para añadir
        pass


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
        if "liked" in self.curr_user and str(self.user["id"]) in str(self.curr_user["liked"]):
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
    
    @command(name='perfil', aliases=['profile'], description="Muestra tu perfil")
    async def _tinder_profile(self, ctx: Context):
        """Ver tu perfil"""
        try:
            user = await (Profile(ctx.author)).get_user_data()
            embed = build_profile(user)
            await ctx.author.send(embed=embed, view=TinderView(self.bot, ctx.author))
        except Exception as e:
            print(e)
            raise CustomError("No tienes un perfil creado `*help Tinder`")
    
    @command(name="tinder", description="Ver los otros perfiles")
    async def _tinder(self, ctx: Context):
        """"""        
        user = await (Profile(ctx.author)).get_user_data()
        try:
            user["id"] = ctx.author.id
        except:
            raise CustomError("No tienes un perfil creado `*help Tinder`")
        users_list = (await tinder_get_list()).stream()
        users = []
        for _user in users_list:
            if int(_user.id) != user["id"] and not \
                ("liked" in user and (str(_user.id) in user["liked"] or int(_user.id) in user["liked"])) and not \
                ("rejected" in user and (str(_user.id) in user["rejected"] or int(_user.id) in user["rejected"])) and not \
                ("matched" in user and (str(_user.id) in user["matched"] or int(_user.id) in user["matched"])):
                    users.append({_user.id: _user.to_dict()})
    
        if len(users) == 0:
            raise CustomError("No hay nadie más para ver")
        
        curr_user = users[0]
        curr_user_id = list(curr_user.keys())[0]
        await ctx.author.send(embed=build_profile(curr_user[curr_user_id]), view=PersistentView(self.bot, user, users, ctx.author))
    
    @command(name="deltinder", description="Elimina tu perfil")
    async def _deltinder(self, ctx: Context):
        """"""
        user = await self.__get_user_data(ctx.author.id)
        try:
            user["id"] = ctx.author.id
        except:
            raise CustomError("No tienes un perfil creado `*help Tinder`")
        await ctx.channel.send("Estás seguro de que quieres eliminar tu perfil? Escribe `confirmar` para confirmar")
        def check(m):
            return m.content.lower().strip() == f'confirmar' and m.channel == ctx.channel and m.author.id == ctx.author.id
        try:
            await self.bot.wait_for('message', check=check, timeout=60.0)
            await tinder_delete(user)
            await ctx.channel.send('Usuario borrado correctamente')
        except asyncio.TimeoutError:
            await ctx.channel.send('Time Out')
            raise CustomError('Ha ocurrido un error borrando el usuario, contacta con <@355104003572498435> `Alguien#8623` porfavor.')
    
    """ @command(name="tindertop")
    async def _tindertop(self, ctx: Context):
        users_list = (await tinder_get_list()).stream()
        users = []
        for _user in users_list:
            user = _user.to_dict()
            if "matched" in user:
                users.append({_user.id: len(user["matched"])})
        print(users) """
    
    """@command(name="set_match")
    async def _set_match(self, ctx: Context):
        revised = []
        users_list = (await tinder_get_list()).stream()
        print('users_list', users_list)
        for _user in users_list:
            print('REVISING USER: ' + str(_user.id))
            user_data = _user.to_dict()
            if "liked" in user_data:
                for _user2 in user_data["liked"]:
                    if int(_user2) not in revised:
                        user2_data = (await tinder_get_user(int(_user2))).get().to_dict()
                        if user2_data is not None:
                            if "liked" in user2_data and (int(_user.id) in user2_data["liked"] or str(_user.id) in user2_data["liked"]):
                                print("Match:", _user2)
                                await tinder_match(int(_user.id), int(_user2))
            revised.append(int(_user.id))
            print('REVISED')"""


async def setup(bot: Bot) -> None:
    await bot.add_cog(Tinder(bot))
