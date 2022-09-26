import discord
from discord.ext.commands import Context
from utils.ddbb.economy import item_save

"""
nombre: str
precio: int
descripcion: str
icon: ?str
"""
class Item():
    def __init__(self, name:str, price:int, description:str = None, icon:str = None) -> None:
        self.name = name
        self.price = price
        self.desc = description
        self.icon = icon
        pass
    
    async def save(self, guild_id:int):
        await item_save(guild_id, {'name':self.name, 'price':self.price, 'desc':self.desc, 'icon':self.icon, 'user': None, 'created_at': None})


class ItemModal(discord.ui.Modal):
    def __init__(self, view, item: Item):
        self.view = view
        self.item = item
        super().__init__(title="Crear nuevo objeto")
        self.name = discord.ui.TextInput(label="Nombre", style=discord.TextStyle.short, placeholder="Nombre del objeto", required=True, row=1, default='' if not hasattr(item, 'name') else item.name)
        self.price = discord.ui.TextInput(label="Precio (número)", style=discord.TextStyle.short, placeholder="Precio del objeto  (número sin puntos ni comas)", required=True, row=2, default='0' if not hasattr(item, 'price') else item.price)
        self.description = discord.ui.TextInput(label="Descripción", style=discord.TextStyle.long, placeholder="Descripción del objeto", required=False, row=3, max_length=250, default='' if not hasattr(item, 'desc') else item.desc)
        self.add_item(self.name)
        self.add_item(self.price)
        self.add_item(self.description)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            name = self.name.value.strip()
            price = int(self.price.value)
            description = self.description.value.strip()
            self.view.item = Item(name, price, description)
            self.stop()
            await self.view.modal_success(interaction)
        except Exception as e:
            print('error:', e)
        return await super().on_submit(interaction)
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print('Error:', error)
        return await super().on_error(interaction, error)

class ItemView(discord.ui.View):
    def __init__(self, guild:discord.guild, item = None):
        super().__init__(timeout=60)
        self.guild = guild
        self.item = item
    
    @discord.ui.button(label='tets', style=discord.ButtonStyle.blurple)
    async def btn(self, interaction, button):
        modal = ItemModal(self, self.item)
        await interaction.response.send_modal(modal)
    
    async def modal_success(self, interaction: discord.Interaction):
        await self.item.save(self.guild.id)
        await interaction.response.edit_message(embed=discord.Embed(title='Objeto creado', description='El objeto ha sido creado correctamente', color=discord.Color.green()), view=None)
        return await super().modal_success(interaction)

async def item_create(ctx: Context):
    embed = discord.Embed(title="Crear Objeto", description="Pulsa el siguiente botón para rellenar los campos Nombre, Precio y Descripción del objeto\nUna vez realizado podrás enviar un emoticono (opcional) para el nuevo objeto", color=0x00ff00)
    await ctx.channel.send(embed=embed, view=ItemView(guild=ctx.guild))
    pass


async def item_delete(ctx: Context):
    pass


async def item_edit(ctx: Context):
    pass