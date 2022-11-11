from asyncio import create_task, sleep
import random
import discord
from discord.ext.commands import *
from enum import Enum
from utils.ddbb.economy import has_money
from utils.errors import CustomError, MoneyError
from utils.logs.economy import lose_money
from utils.responses.Embed import Embed


class Difficulty(Enum):
    PEACEFULL = 0
    KICK = 1
    BAN = 2

class Gamemode(Enum):
    ONE_DEATH = 0
    ONE_SURVIVOR = 1

def get_embed(rules: object):
    embed = Embed(title='RUSSIAN ROULETTE', description=f'Segundos restantes: {rules["time"]}s').warn()
    difficulty = 'PACÍFICO' if str(rules["difficulty"]) == str(Difficulty.PEACEFULL) else 'KICK' if str(rules["difficulty"]) == str(Difficulty.KICK) else 'BAN'
    gamemode = 'UNA MUERTE' if str(rules["gamemode"]) == str(Gamemode.ONE_DEATH) else 'UN SUPERVIVIENTE'
    embed.add_field(title='REGLAS', desc=f'Dificultad: {difficulty}\nGamemode: {gamemode}\nApuesta: {rules["ammount"]} 💰\nPremio: {rules["ammount"] * len(rules["players"])} 💰')
    desc = ''
    for player in rules['players']:
        desc+=f'{player["name"]}\n'
    embed.add_field(title=f'JUGADORES: {len(rules["players"])}', desc=desc)
    return embed.get_embed()


class RRGame():
    def __init__(self, bot: Bot, game_id: str) -> None:
        self.bot = bot
        global games
        game = games[game_id]
        self.game_id = game_id
        self.ammount = game['ammount']
        self.channel = game['channel']
        self.difficulty = game['difficulty']
        self.gamemode = game['gamemode']
        self.guild = game['guild']
        self.players = game['players']
        self.player_list = game['players']
        self.round = 0
    
    def embed(self):
        embed = Embed(title='RUSSIAN ROULETTE', description='**SIGUIENTE RONDA**').warn()
        desc = ''
        j = 0
        for i in range(0, len(self.player_list)-1):
            if self.player_list[i]['id'] == self.players[i-j]['id']:
                desc+=f'{self.players[i-j]["name"]}\n'
            else:
                j-=1
                desc+=f'~~{self.players[i-j]["name"]}~~\n'
        embed.add_field(title=f'JUGADORES VIVOS: {len(self.players)}', desc=desc)
        return embed.get_embed()
    
    async def start(self):
        ended = False
                    
        while not ended:
            num = random.randint(0, len(self.players)-1)
            for i in range(0, len(self.players)):
                if i == num:
                    player = self.players[i]
                    del self.players[i]
                    await (await self.bot.fetch_channel(int(self.channel))).send(embed=Embed(description=f'{player["name"]} se muere ☠️').get_embed())
                    if self.difficulty == 'Difficulty.KICK':
                        try:
                            await (await self.bot.fetch_guild(self.guild)).kick(discord.Object(player["id"]), reason="Russian Roulette")
                        except discord.Forbidden as e:
                            raise e
                    elif self.difficulty == 'Difficulty.BAN':
                        try:
                            await (await self.bot.fetch_guild(self.guild)).ban(discord.Object(player["id"]), reason="Russian Roulette")
                        except discord.Forbidden as e:
                            raise e
                    
                    if self.gamemode == Gamemode.ONE_DEATH:
                        ended = True
                        await self.end()
                        break
                    else:
                        if len(self.players) <= 1:
                            ended = True
                            await self.end()
                            break
                        else:
                            await sleep(1)
                            break
                else:
                    await (await self.bot.fetch_channel(int(self.channel))).send(embed=Embed(description=f'**{self.players[i]["name"]}** se salva ✝️').get_embed())
                    await sleep(0.8)
            if len(self.players) > 1:
                await (await self.bot.fetch_channel(int(self.channel))).send(embed=Embed(description=f'SIGUIENTE RONDA: **{len(self.players)} jugadores** restantes\nEmpezando en 2 segundos').warn().get_embed())
            await sleep(2)

    async def end(self):
        global games
        del games[self.game_id]
        embed = Embed(title='RUSSIAN ROULETTE').success()
        embed.description = '**GANADORES**\n' if len(self.players) > 1 else '**GANADOR**\n' if len(self.players) == 1 else 'Que triste, jugaste solo y te moriste'
        try:
            money = int(self.ammount * len(self.player_list) / len(self.players))
        except:
            pass
        for player in self.players:
            embed.description += f'<@{player["id"]}> {"" if money == 0 else str(money) + " 💰"}\n'
        await (await self.bot.fetch_channel(int(self.channel))).send(embed=embed.get_embed())
        return


class DifficultySelect(discord.ui.Select):
    def __init__(self, game, rr_view, bot):
        self.bot = bot
        self.game = game
        self.rr_view = rr_view
        options = [
            discord.SelectOption(label='PACÍFICO', value=str(Difficulty.PEACEFULL), default=True),
            discord.SelectOption(label='KICK', value=str(Difficulty.KICK)),
            discord.SelectOption(label='BAN', value=str(Difficulty.BAN)),
        ]
        super().__init__(placeholder='DIFICULTAD', min_values=1, max_values=1, options=options, row=1)

    def set_default(self):
        if str(self.game['difficulty']) == str(Difficulty.PEACEFULL):
            self.options[0].default = True
            self.options[1].default = False
            self.options[2].default = False
        elif str(self.game['difficulty']) == str(Difficulty.KICK):
            @discord.ext.commands.bot_has_guild_permissions(kick_members=True)
            def update_kick():
                self.options[0].default = False
                self.options[1].default = True
                self.options[2].default = False
            
            update_kick()
        elif str(self.game['difficulty']) == str(Difficulty.BAN):
            @discord.ext.commands.bot_has_guild_permissions(ban_members=True)
            def update_ban():
                self.options[0].default = False
                self.options[1].default = False
                self.options[2].default = True
            update_ban()
        else:
            raise CustomError('Fail Selecting Difficulty')
    
    async def callback(self, interaction: discord.Interaction):
        self.set_default()
        await interaction.response.edit_message(embed=get_embed(self.game), view=self.rr_view)

class GamemodeSelect(discord.ui.Select):
    def __init__(self, game, rr_view):
        self.game = game
        self.rr_view = rr_view
        options = [
            discord.SelectOption(label='UNA MUERTE', value=str(Gamemode.ONE_DEATH), default=True),
            discord.SelectOption(label='UN SUPERVIVIENTE', value=str(Gamemode.ONE_SURVIVOR))
        ]
        super().__init__(placeholder='GAMEMODE', min_values=1, max_values=1, options=options, row=2)

    def set_default(self):
        if str(self.game['gamemode']) == str(Gamemode.ONE_DEATH):
            self.options[0].default = True
            self.options[1].default = False
        elif str(self.game['gamemode']) == str(Gamemode.ONE_SURVIVOR):
            self.options[0].default = False
            self.options[1].default = True
        else:
            raise CustomError('Fail Selecting Gamemode')
    
    async def callback(self, interaction: discord.Interaction):
        self.set_default()
        await interaction.response.edit_message(embed=get_embed(self.game), view=self.rr_view)

class RRView(discord.ui.View):
    def __init__(self, bot, game_id: str):
        super().__init__(timeout=60)
        self.bot = bot
        global games
        self.game_id = game_id
        self.gamemode_select = GamemodeSelect(games[game_id], self)
        self.add_item(self.gamemode_select)
        self.difficulty_select = DifficultySelect(games[game_id], self, self.bot)
        self.add_item(self.difficulty_select)
        self.exit = False
        self.task = create_task(self.timer())
    
    @discord.ui.button(label='Jugar', style=discord.ButtonStyle.green, custom_id='join', row=3)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.in_game(interaction.user.id):
            return await interaction.response.send_message('Ya estás en la partida!', ephemeral=True)
        
        global games
        game = games[str(self.game_id)]
        if not await has_money(game['guild'], interaction.user.id, game['ammount']):
            return await interaction.response.send_message('No tienes suficiente dinero', ephemeral=True)
        games[str(self.game_id)]['players'].append({'name': interaction.user.display_name, 'id': interaction.user.id})
        
        await interaction.response.send_message(content='Entraste correctamente!', ephemeral=True)
        await self.message.edit(embed=get_embed(games[str(self.game_id)]), view=self)

    @discord.ui.button(label='Salir', style=discord.ButtonStyle.red, custom_id='exit', row=3)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        global games
        if interaction.user.id == games[self.game_id]['author']:
            if not self.exit:
                self.exit = True
                return await interaction.response.send_message('Seguro quieres cancelar la partida? Si es así, vuelve a pulsar el botón de salir')
            else:
                self.task.cancel()
                del games[self.game_id]
                self.stop()
                return await interaction.response.edit_message(embed=Embed(description=f'Partida cancelada por {interaction.user.mention}').failure().get_embed(), view=None)
                
        if not self.in_game(interaction.user.id):
            return await interaction.response.send_message('No estás en la partida', ephemeral=True)
        
        i = 0
        for user in games[self.game_id]['players']:
            if int(user['id']) == interaction.user.id:
                del games[self.game_id]['players'][i]
            i+=1
        
        await interaction.response.send_message(content='Saliste correctamente!', ephemeral=True)
        await self.message.edit(embed=get_embed(games[str(self.game_id)]), view=self)
        
    
    @discord.ui.button(label='Empezar', style=discord.ButtonStyle.blurple, row=3)
    async def start_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        global games
        if interaction.user.id != games[self.game_id]['author']:
            return await interaction.response.send_message('Solo el creador de la partida la puede iniciar!', ephemeral=True)
        self.task.cancel()
        await interaction.response.send_message(content='Juego empezado correctamente!', ephemeral=True)
        await self.init_game()
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        global games
        
        if len(self.difficulty_select.values) > 0 and self.difficulty_select.values[0] != games[self.game_id]['difficulty']:
            if interaction.user.id != games[self.game_id]['author']:
                await interaction.response.send_message('Solo el creador de la partida la puede cambiar la dificultad del juego!', ephemeral=True)
                return False
            else:
                games[self.game_id]['difficulty'] = self.difficulty_select.values[0]

        if len(self.gamemode_select.values) > 0 and self.gamemode_select.values[0] != games[self.game_id]['gamemode']:
            if interaction.user.id != games[self.game_id]['author']:
                await interaction.response.send_message('Solo el creador de la partida la puede cambiar el modo de juego!', ephemeral=True)
                return False
            else:
                games[self.game_id]['gamemode'] = self.gamemode_select.values[0]
        return await super().interaction_check(interaction)
    
    async def on_timeout(self) -> None:
        await self.message.edit(view=None)
        await self.init_game()
    
    def in_game(self, user_id):
        global games
        for user in games[self.game_id]['players']:
            if int(user['id']) == user_id:
                return True
        return False
    
    async def init_game(self):
        self.stop()
        game = RRGame(self.bot, self.game_id)
        await game.start()

    async def timer(self):
        global games
        times = [10, 10, 10, 10, 5, 5, 5, 2, 1, 1]
        for time in times:
            self.sleep = await sleep(time)
            games[self.game_id]["time"] -= time
            await self.message.edit(embed=get_embed(games[self.game_id]))
        

async def russian_roulette(bot: Bot, ctx: Context, money: int = 0):
    try:
        money = int(money)
        if money < 0:
            raise MoneyError(min=0)
    except:
        money = 0
    
    global games
    if not 'games' in globals():
        games = {}
    if str(ctx.channel.id) in games:
        raise CustomError('Ya hay una partida en juego!')
    
    games[str(ctx.channel.id)] = {'difficulty': Difficulty.PEACEFULL, 'gamemode': Gamemode.ONE_DEATH, 'ammount': money, 'time': 60, 'guild': ctx.guild.id, 'channel': ctx.channel.id, 'author':ctx.author.id, 'players': [{'name': ctx.author.display_name, 'id': ctx.author.id}]}
    
    view = RRView(bot, str(ctx.channel.id))
    view.message = await ctx.channel.send(embed=get_embed(games[str(ctx.channel.id)]), view=view)