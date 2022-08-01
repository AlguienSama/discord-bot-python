import discord
from discord.ext import commands
from utils.ddbb.games import oj_get_card, oj_set_card
from utils.errors import CustomError

from utils.responses.Embed import Embed

class Card():
    def __init__(self, guild: discord.guild, user: discord.User, data: object) -> None:
        if data is None:
            self.life = 5
            self.damage = 0
            self.defense = 0
            self.dodge = 0
        else:
            self.life = data['life']
            self.damage = data['damage']
            self.defense = data['defense']
            self.dodge = data['dodge']
        
        self.base_points = 6
        self.option = None
        self.user = user
        self.guild = guild
    
    async def save(self) -> None:
        await oj_set_card(self.guild.id, self.user.id, {'life': self.life, 'damage': self.damage, 'defense': self.defense, 'dodge': self.dodge})
    
    def restant_points(self):
        return self.base_points - self.life - self.damage - self.defense - self.dodge

    def get_embed(self) -> discord.Embed:
        embed = Embed(title='OJ Game', description='Selecciona una opción', color=0x1B8D2C)
        embed.set_author(name=f'{self.user.display_name}', icon_url=self.user.avatar.url)
        
        embed.add_field(title=f'{"▶️ " if self.option == "life" else ""}💖 Vida: {self.life}', desc='_ _', inline=True)
        embed.add_field(title=f'{"▶️ " if self.option == "damage" else ""}🗡 Daño: {self.damage}', desc='_ _', inline=True)
        embed.add_field(title=f'{"▶️ " if self.option == "defense" else ""}🛡 Defensa: {self.defense}', desc='_ _', inline=True)
        embed.add_field(title=f'{"▶️ " if self.option == "dodge" else ""}💨 Esquive: {self.dodge}', desc='_ _', inline=True)
        embed.add_field(title=f'🎲 Puntos restantes: {self.restant_points()}', desc='_ _', inline=True)
        
        return embed.get_embed()


class Select(discord.ui.Select):
    def __init__(self, user_card: Card) -> None:
        options = [
            discord.SelectOption(label='Vida', emoji='💖', value='life'),
            discord.SelectOption(label='Daño', emoji='🗡', value='damage'),
            discord.SelectOption(label='Defensa', emoji='🛡', value='defense'),
            discord.SelectOption(label='Esquive', emoji='💨', value='dodge'),
        ]
        self.user_card = user_card
        super().__init__(placeholder='Selecciona una opción', options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.user_card.get_embed())

class Button(discord.ui.Button):
    def __init__(self, style):
        super().__init__(style)

class SelectView(discord.ui.View):
    def __init__(self, user_card: Card) -> None:
        super().__init__(timeout=60.0)
        self.user_card = user_card
        self.select = Select(user_card)
        self.add_item(self.select)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        check = interaction.user.id == self.user_card.user.id
        if check is False:
            await interaction.response.send_message(content=f'No puedes editar una carta que no sea tuya!', ephemeral=True)
            return False
        try:
            self.user_card.option = self.select.values[0]
            return True
        except:
            await interaction.response.send_message(content='Selecciona una opción', ephemeral=True)
            return False
    
    async def on_timeout(self) -> None:
        await self.msg.edit(embed=self.user_card.get_embed(), view=None)
    
    @discord.ui.button(label='Sumar', emoji='\U00002B06', style=discord.ButtonStyle.gray, custom_id='select_view:grey')
    async def up(self, interaction: discord.Interaction, button: discord.ui.Button):
        attr = getattr(self.user_card, self.user_card.option)
        print(self.user_card.option)
        if self.user_card.option == 'life' and self.user_card.life >= 7 or (self.user_card.option != 'life' and attr >= 2):
            await interaction.response.send_message(content='No puedes sumar más puntos en la opción', ephemeral=True)
        elif self.user_card.restant_points() <= 0:
            await interaction.response.send_message(content='No tienes más puntos para sumar', ephemeral=True)
        else:
            setattr(self.user_card, self.user_card.option, attr + 1)
            await self.user_card.save()
            await interaction.response.edit_message(embed=self.user_card.get_embed())
    
    @discord.ui.button(label='Restar', emoji='\U00002B07', style=discord.ButtonStyle.grey, custom_id='select_view:gray')
    async def down(self, interaction: discord.Interaction, button: discord.ui.Button):
        attr = getattr(self.user_card, self.user_card.option)
        if self.user_card.option == 'life' and self.user_card.life <= 3 or (self.user_card.option != 'life' and attr <= -2):
            await interaction.response.send_message(content='No puedes restar más puntos en la opción', ephemeral=True)
        else:
            setattr(self.user_card, self.user_card.option, attr - 1)
            await self.user_card.save()
            await interaction.response.edit_message(embed=self.user_card.get_embed())


async def oj_card(ctx: commands.Context):
    """ """
    user_card = await oj_get_card(ctx.guild.id, ctx.author.id)
    user_card = Card(ctx.guild, ctx.author, user_card)
    
    view = SelectView(user_card)
    view.msg = await ctx.send(embed=user_card.get_embed(), view=view)
    pass