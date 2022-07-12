import discord
from discord.ext.commands import *
from random import randint
from utils.responses.Embed import Embed


class Card:
    def __init__(self, user) -> None:
        self.life = 5
        self.damage = 0
        self.defense = 0
        self.dodge = 0
        self.username = user
    
    async def update(self):
        # get stats from db
        pass


class DefendAction(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=20.0)


class Game:
    def __init__(self, player1: discord.User, player2: discord.User, channel: discord.TextChannel) -> None:
        self.channel = channel
        self.user1 = player1
        self.user2 = player2
        self.player1 = Card(player1).update()
        self.player2 = Card(player2).update()
        self.attack = None
        self.deffend = None
        self.turn = 0
        self.turn_calc = 0
        self.msg = None
    
    async def start(self):
        self.set_turn()
        total_damage = self.attack.damage + self.rand_dice()
        if self.msg is None:
            self.msg = await self.channel.send(embed=self.embed(total_damage), view=DefendAction())
        await self.msg.edit(embed=self.embed(total_damage))
        
        # defense or dodge
        if 'defense':
            total_defense = self.deffend.defense + self.rand_dice()
            damage = total_damage - total_defense
            self.deffend.life -= damage if damage > 0 else 1
        elif 'dodge':
            total_dodge = self.deffend.dodge + self.rand_dice()
            self.deffend.life -= total_damage if total_damage >= total_dodge else 0
        
        if self.winner():
            return self.winner()
        else:
            self.start()
        pass
    
    def rand_dice(self):
        return randint(1, 6)
    
    def set_turn(self):
        if self.turn_calc == 0:
            self.turn_calc = randint(1, 2)
        
        if self.turn_calc == 1:
            self.turn_calc = 2
            self.attack = self.player1
            self.deffend = self.player2
        else:
            self.turn_calc = 1
            self.attack = self.player2
            self.deffend = self.player1
        self.turn += 1
        pass

    def get_users(self):
        if self.turn_calc == 1:
            return self.user1, self.user2
        else:
            return self.user2, self.user1
    
    def winner(self):
        if self.player1.life <= 0:
            return self.player2
        elif self.player2.life <= 0:
            return self.player1
        else:
            return False
        
    def embed(self, damage=0):
        def description(user):
            return f'**💖 {user.life}**\n🗡 {user.damage}\n🛡 {user.defense}\n🌪 {user.dodge}'
        
        attack, defense = self.get_users()
        embed = Embed(title='OJ Game', description=f'Turno: {self.turn}\nAtacante: {attack.mention}\nDefensor: {defense.mention}').add_field(name=f'{self.user1}', value=description(self.player1)).add_field(name=f'{self.user2}', value=description(self.player2)).add_field(name='Acciones', value=f'Daño de **{attack}**: {self.attack.damage} + 🎲 {damage-self.attack.damage} = {damage}\nQue acción desea realizar **{defense}**?')
        return embed.get_embed()


class AcceptGame(discord.ui.View):
    def __init__(self, author: discord.User, channel: discord.TextChannel):
        super().__init__(timeout=60.0)
        self.author = author
        self.channel = channel
    
    async def on_timeout(self) -> None:
        await self.channel.send(f'Tiempo de espera finalizado.')
        return await super().on_timeout()
        
    @discord.ui.button(label='Aceptar', emoji='\U00002705', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.edit_message(content='Vamos a empezar!')
            await self.channel.send(f'{interaction.user.mention} aceptó el juego!')
            self.stop()
            await Game(self.author, interaction.user, self.channel).start()
            return interaction.user
        else:
            await interaction.response.send_message(content='No puedes jugar contra ti mismo!', ephemeral=True)

async def oj_game(ctx: Context):
    """ """
    await ctx.send('Esperando rival para jugar...', view=AcceptGame(ctx.author, ctx.channel))
    pass
