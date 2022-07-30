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
        self.user = user
    
    def update(self):
        # get stats from db
        return self


class DefendAction(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=20.0)
        self.Game = game
    
    @discord.ui.button(label='Defender', emoji='\U0001F6E1', style=discord.ButtonStyle.green, custom_id='defend_action:green')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=f'Defensor: {self.Game.attack.user.mention}')
        self.stop()
        await self.Game.action('defend')

    @discord.ui.button(label='Esquivar', emoji='\U0001F4A8', style=discord.ButtonStyle.blurple, custom_id='defend_action:blue')
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=f'Defensor: {self.Game.attack.user.mention}')
        self.stop()
        await self.Game.action('dodge')

    @discord.ui.button(label='Rendirse', emoji='\U00002716', style=discord.ButtonStyle.red, custom_id='defend_action:red')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=f'Defensor: {self.Game.attack.user.mention}')
        self.stop()
        await self.Game.action('surrender')

    async def interaction_check(self, interacion: discord.Interaction) -> bool:
        return interacion.user.id == self.Game.deffend.user.id

    async def on_timeout(self) -> None:
        return await super().on_timeout()

    async def on_error(self, interaction: discord.Interaction, error: Exception, item) -> None:
        print('Error:', error)
        self.stop()
        return await super().on_error(interaction, error, item)


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
        self.total_damage = 0
        self.last_turn_damage = 0
        self.last_turn_action = None
    
    async def start(self):
        self.set_turn()
        self.last_turn_damage = self.total_damage
        self.total_damage = self.attack.damage + self.rand_dice()
        if self.msg is None:
            self.msg = await self.channel.send(content=f'Defensor: {self.deffend.user.mention}', embed=self.embed(), view=DefendAction(self))
        else:
            await self.msg.edit(embed=self.embed(), view=DefendAction(self))
    
    async def action(self, action):
        if action == 'defend':
            total_defense = self.deffend.defense + self.rand_dice()
            damage = self.total_damage - total_defense
            self.last_turn_action = f'**Defendido** con {self.deffend.defense} + 🎲 {total_defense - self.deffend.defense} = **{total_defense}**'
            realized_damage = damage if damage > 0 else 1
            self.last_turn_action += f'\nDaño realizado: {realized_damage}'
            self.deffend.life -= realized_damage
        elif action == 'dodge':
            total_dodge = self.deffend.dodge + self.rand_dice()
            dodged = self.total_damage < total_dodge
            self.last_turn_action = f'**Esquivado** con {self.deffend.dodge} + 🎲 {total_dodge - self.deffend.dodge} = **{"ÉXITO" if dodged else "FALLIDO"}**'
            self.deffend.life -= 0 if dodged else self.total_damage
        else:
            self.last_turn_action = F'**Rendido**'
            self.last_turn_action = f'**Rendido**'
            self.deffend.life = 0
        
        if self.winner():
            await self.end_game()
        else:
            await self.start()
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
    
    def embed_user_data(self, user):
        return f'**💖 {user.life}**\n🗡 {user.damage}\n🛡 {user.defense}\n💨 {user.dodge}'
    
    async def end_game(self):
        embed = Embed(title='OJ Game', description=f'{self.user1.mention} vs {self.user2.mention}\n**GANADOR: {self.attack.user.mention}** # Turno **{self.turn}**').add_field(title=f'{self.user1}', desc=self.embed_user_data(self.player1), inline=True).add_field(title=f'{self.user2}', desc=self.embed_user_data(self.player2), inline=True).add_field(title='Movimiento anterior', desc=f'Daño de **{self.deffend.user}**: {self.deffend.damage} + 🎲 {self.last_turn_damage-self.deffend.damage} = **{self.last_turn_damage}**\nAcción de **{self.attack.user}**: {self.last_turn_action}').success()
        await self.msg.edit(content=f'**{self.attack.user.mention}** gana la partida!', embed=embed.get_embed())
        
    def embed(self):
        embed = Embed(title='OJ Game', description=f'Turno: {self.turn}\nAtacante: {self.attack.user.mention}\nDefensor: {self.deffend.user.mention}').add_field(title=f'{self.user1}', desc=self.embed_user_data(self.player1), inline=True).add_field(title=f'{self.user2}', desc=self.embed_user_data(self.player2), inline=True)
        if self.last_turn_action is not None:
            embed.add_field(title='Movimiento anterior', desc=f'Daño de **{self.deffend.user}**: {self.deffend.damage} + 🎲 {self.last_turn_damage-self.deffend.damage} = **{self.last_turn_damage}**\nAcción de **{self.attack.user}**: {self.last_turn_action}')
        embed.add_field(title='Movimiento', desc=f'Daño de **{self.attack.user}**: {self.attack.damage} + 🎲 {self.total_damage-self.attack.damage} = **{self.total_damage}**\nQue acción desea realizar **{self.deffend.user}**?')
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
        else:
            await interaction.response.send_message(content='No puedes jugar contra ti mismo!', ephemeral=True)

async def oj_game(ctx: Context):
    """ """
    await ctx.send('Esperando rival para jugar...', view=AcceptGame(ctx.author, ctx.channel))
    pass
