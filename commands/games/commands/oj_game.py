import time
import discord
from discord.ext.commands import *
from random import randint
from utils.ddbb.games import oj_get_card
from utils.responses.Embed import Embed

moeru = 800480469678162011

class Card:
    def __init__(self, guild, user) -> None:
        self.life = 5
        self.damage = 0
        self.defense = 0
        self.dodge = 0
        self.user = user
        self.guild = guild
    
    async def update(self):
        if self.user.id == moeru:
            return self.set_ai_data()
        try:
            data = await oj_get_card(self.guild.id, self.user.id)
            self.life = data['life']
            self.damage = data['damage']
            self.defense = data['defense']
            self.dodge = data['dodge']
        except:
            return self
    
    def restant_points(self):
        return 6 - self.life - self.damage - self.defense - self.dodge

    def set_ai_data(self):
        props = ['life', 'damage', 'defense', 'dodge']
        
        def plus():
            prop = props[randint(0, 3)]
            if prop == 'life' and self.life >= 7:
                plus()
            elif (prop == 'damage' or prop == 'defense' or prop == 'dodge') and getattr(self, prop) >= 2:
                plus()
            val = getattr(self, prop)
            setattr(self, prop, val + 1)
            if self.restant_points() > 0:
                plus()
            return
        def minus():
            prop = props[randint(0, 3)]
            if prop == 'life' and self.life <= 3:
                minus()
            elif (prop == 'damage' or prop == 'defense' or prop == 'dodge') and getattr(self, prop) <= -2:
                minus()
            val = getattr(self, prop)
            setattr(self, prop, val - 1)
            if self.restant_points() < 0:
                minus()
            return
        
        for i in range(4):
            val = getattr(self, props[i])
            rand = randint(-2, 2)
            if props[i] == 'damage' and rand < 0:
                rand = 1
            setattr(self, props[i], val + rand)
        if self.restant_points() > 0:
            plus()
        elif self.restant_points() < 0:
            minus()
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

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        check = interaction.user.id == self.Game.deffend.user.id
        if check is False:
            await interaction.response.send_message(content=f'El defensor es **{self.Game.deffend.user}**', ephemeral=True)
        return check

    async def on_timeout(self) -> None:
        self.stop()
        await self.Game.action('timeout')
        return await super().on_timeout()

    async def on_error(self, interaction: discord.Interaction, error: Exception, item) -> None:
        print('Error:', error)
        self.stop()
        return await super().on_error(interaction, error, item)


class Game:
    def __init__(self, guild: discord.Guild, player1: discord.User, player2: discord.User, channel: discord.TextChannel) -> None:
        self.channel = channel
        self.user1 = player1
        self.user2 = player2
        self.player1 = Card(guild, player1)
        self.player2 = Card(guild, player2)
        self.attack = None
        self.deffend = None
        self.turn = 0
        self.turn_calc = 0
        self.msg = None
        self.total_damage = 0
        self.last_turn_damage = 0
        self.last_turn_action = None
    
    async def start(self):
        if self.turn == 0:
            await self.player1.update()
            await self.player2.update()
        self.set_turn()
        self.last_turn_damage = self.total_damage
        self.total_damage = self.attack.damage + self.rand_dice()
        if self.total_damage <= 0:
            self.total_damage = 1
        if self.player2.user.id == moeru:
            if self.deffend == self.player2:
                if self.msg is None:
                    self.msg = await self.channel.send(content=f'Defensor: {self.deffend.user.mention}', embed=self.embed(), view=DefendAction(self))
                else:
                    await self.msg.edit(content=f'Defensor: {self.deffend.user.mention}', embed=self.embed(), view=DefendAction(self))
                time.sleep(5)
                if self.total_damage - self.player2.dodge <= 3:
                    await self.action('dodge')
                if self.player2.life == 1:
                    await self.action('dodge')
                else:
                    await self.action('defend')
            else:
                if self.msg is None:
                    self.msg = await self.channel.send(content=f'Defensor: {self.deffend.user.mention}', embed=self.embed(), view=DefendAction(self))
                else:
                    await self.msg.edit(content=f'Defensor: {self.deffend.user.mention}', embed=self.embed(), view=DefendAction(self))
        elif self.msg is None:
            self.msg = await self.channel.send(content=f'Defensor: {self.deffend.user.mention}', embed=self.embed(), view=DefendAction(self))
        else:
            await self.msg.edit(content=f'Defensor: {self.deffend.user.mention}', embed=self.embed(), view=DefendAction(self))
    
    async def action(self, action):
        if action == 'defend':
            total_defense = self.deffend.defense + self.rand_dice()
            if total_defense <= 0:
                total_defense = 1
            damage = self.total_damage - total_defense
            self.last_turn_action = f'**Defendido** con {self.deffend.defense} + 🎲 {total_defense - self.deffend.defense} = **{total_defense}**'
            realized_damage = damage if damage > 0 else 1
            self.last_turn_action += f'\nDaño realizado: **{realized_damage}**'
            self.deffend.life -= realized_damage
        elif action == 'dodge':
            total_dodge = self.deffend.dodge + self.rand_dice()
            dodged = self.total_damage < total_dodge
            self.last_turn_action = f'**Esquivado** con {self.deffend.dodge} + 🎲 {total_dodge - self.deffend.dodge} = **{"ÉXITO" if dodged else "FALLIDO"}**'
            self.deffend.life -= 0 if dodged else self.total_damage if self.total_damage > 0 else 1
        elif action == 'surrender':
            self.last_turn_action = F'**Rendido**'
            self.deffend.life = 0
        elif action == 'timeout':
            self.last_turn_action = F'**AFK**'
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
            if self.player2.user.id == moeru:
                self.attack = self.player2
                self.deffend = self.player1
            else:
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
            self.player1.life = 0
            return self.player2
        elif self.player2.life <= 0:
            self.player2.life = 0
            return self.player1
        else:
            return False
    
    def embed_user_data(self, user):
        return f'**💖 {user.life}**\n🗡 {user.damage}\n🛡 {user.defense}\n💨 {user.dodge}'
    
    async def end_game(self):
        embed = Embed(title='OJ Game', description=f'{self.user1.mention} vs {self.user2.mention}\n**GANADOR: {self.attack.user.mention}** # Turno **{self.turn}**').add_field(title=f'{self.user1}', desc=self.embed_user_data(self.player1), inline=True).add_field(title=f'{self.user2}', desc=self.embed_user_data(self.player2), inline=True).add_field(title='Movimiento anterior', desc=f'Daño de **{self.attack.user}**: {self.attack.damage} + 🎲 {self.total_damage-self.attack.damage} = **{self.total_damage}**\nAcción de **{self.deffend.user}**: {self.last_turn_action}').success()
        await self.msg.edit(content=f'**{self.attack.user.mention}** gana la partida!', embed=embed.get_embed(), view=None)
        
    def embed(self):
        embed = Embed(title='OJ Game', description=f'Turno: {self.turn}\nAtacante: {self.attack.user.mention}\nDefensor: {self.deffend.user.mention}').add_field(title=f'{self.user1}', desc=self.embed_user_data(self.player1), inline=True).add_field(title=f'{self.user2}', desc=self.embed_user_data(self.player2), inline=True)
        if self.last_turn_action is not None:
            embed.add_field(title='Movimiento anterior', desc=f'Daño de **{self.deffend.user}**: {self.deffend.damage} + 🎲 {self.last_turn_damage-self.deffend.damage} = **{self.last_turn_damage}**\nAcción de **{self.attack.user}**: {self.last_turn_action}')
        embed.add_field(title='Movimiento', desc=f'Daño de **{self.attack.user}**: {self.attack.damage} + 🎲 {self.total_damage-self.attack.damage} = **{self.total_damage}**\nQue acción desea realizar **{self.deffend.user}**?')
        return embed.get_embed()


class AcceptGame(discord.ui.View):
    def __init__(self, guild: discord.Guild, author: discord.User, channel: discord.TextChannel):
        super().__init__(timeout=60.0)
        self.author = author
        self.channel = channel
        self.guild = guild
    
    async def on_timeout(self) -> None:
        await self.msg.edit(content=f'Tiempo de espera finalizado.', view=None)
    
        
    @discord.ui.button(label='Aceptar', emoji='\U00002705', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.edit_message(content='Vamos a empezar!', view=None)
            await self.channel.send(f'{interaction.user.mention} aceptó el juego!')
            self.stop()
            await Game(self.guild, self.author, interaction.user, self.channel).start()
        else:
            await interaction.response.send_message(content='No puedes jugar contra ti mismo!', ephemeral=True)
    
    @discord.ui.button(label='VS Moeru', style=discord.ButtonStyle.secondary, custom_id='persistent_view:blue')
    async def vs_ui(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.author:
            await interaction.response.edit_message(content='Vamos a empezar!', view=None)
            user = await self.guild.fetch_member(moeru)
            await self.channel.send(f'Partida contra {user.mention}!')
            self.stop()
            await Game(self.guild, self.author, user, self.channel).start()
        else:
            await interaction.response.send_message(content='No puedes seleccionar esta opción!', ephemeral=True)

async def oj_game(ctx: Context):
    """ """
    view = AcceptGame(ctx.guild, ctx.author, ctx.channel)
    view.msg = await ctx.send('Esperando rival para jugar...', view=view)
    pass
