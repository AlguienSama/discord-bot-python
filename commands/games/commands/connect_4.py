from discord.ext.commands import *
from discord import User
import asyncio
from utils.errors import CustomError

async def conenct_4(bot: Bot, ctx: Context):
    await ctx.channel.send(f'Esperando que el oponente acepte la partida `{ctx.prefix}a` (60 segundos)')
    
    def check(m):
        return m.content == f'{ctx.prefix}a' and m.channel == ctx.channel and m.author.id != ctx.author.id
    
    user = None
    try:
        user = await bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.channel.send('Time Out')
        raise CustomError('No puede jugar en soledad, lo siento.')
    else: 
        message = await ctx.channel.send('Recuerda que debes de enviar el número correspondiene a la casilla donde quieras poner la ficha...')
    
    user = user.author
    if user is None:
        raise CustomError('Invalid Player')
    
    [red, yellow] = [':red_circle:', ':yellow_circle:']
    
    game = Connect_4(bot, ctx, message, ctx.author, user, red, yellow)
    await game.start()
    

class Connect_4:
    def __init__(self, bot: Bot, ctx: Context, message, player1: User, player2: User, red: str = ':red_circle:', yellow: str = ':yellow_circle:'):
        self.bot = bot
        self.ctx = ctx
        self.board = [[],[],[],[],[],[]]
        for i in range(6):
            self.board[i] = [':black_large_square:' for j in range(7)]
        self.positions = [5 for i in range(7)]
        self.channel = ctx.channel
        self.player1 = player1
        self.player2 = player2
        self.piece1 = red
        self.piece2 = yellow
        self.turn = 1
        self.game = 1
        self.message = message
    
    def check_turn(self, m):
        try:
            return m.channel == self.channel and \
                m.author.id == (self.player1.id if self.turn == 1 else self.player2.id) and \
                self.positions[int(m.content)-1] >= 0
        except:
            return False
    
    async def start(self):
        while self.game == 1:
            player = self.player1 if self.turn == 1 else self.player2
            piece = self.piece1 if self.turn == 1 else self.piece2
            await self.msg_send(player, piece)
            
            try:
                content = await self.bot.wait_for('message', check=self.check_turn, timeout=15.0)
                index = int(content.content)-1
                self.board[self.positions[index]][index] = piece
                self.positions[index]-=1
                await self.msg_send(player, piece)
            except asyncio.TimeoutError:
                await self.channel.send(f'Time Out, Loser : {player}')
                return
            else:
                self.turn *= -1
                await content.delete()
                if self.win():
                    self.game = 0
                    await self.msg_win(player, piece)
                if self.draw():
                    self.game = 0
                    await self.msg_draw()
    
    def msg_board(self) -> str:
        msg = ""
        for row in self.board:
            msg += " ".join(row) + "\n"
        msg += ':one: :two: :three: :four: :five: :six: :seven:'
        return msg
    
    async def msg_send(self, player, piece):
        msg = f'**CONNECT 4**\nTurno de *{player} {piece}*\n' \
            f'Tiempo límite de 15 segundos para hacer tu movimiento' \
            f'\n{self.msg_board()}'
        await self.message.edit(content=msg)
    
    async def msg_draw(self):
        msg = f'**!!EMPATE!!**\n\n{self.msg_board()}'
        await self.message.edit(content=msg)
    
    async def msg_win(self, player, piece):
        msg = f'**!!VICTORIA de {player} {piece}!!**\n' \
            f'\n{self.msg_board()}'
        await self.message.edit(content=msg)
        
    def win(self) -> bool:
        # rows
        for row in range(6):
            piece = ''
            times = 0
            for col in range(7):
                if piece != self.board[row][col] and self.board[row][col] != ':black_large_square:':
                    piece = self.board[row][col]
                    times = 1
                elif piece == self.board[row][col]:
                    times+=1
                
                if times == 4:
                    return True
                
        # cols
        for col in range(7):
            piece = ''
            times = 0
            for row in range(6):
                if piece != self.board[row][col] and self.board[row][col] != ':black_large_square:':
                    piece = self.board[row][col]
                    times = 1
                elif piece == self.board[row][col]:
                    times+=1
                
                if times == 4:
                    return True
                
        # diagonal down
        for row in range(6):
            piece = ''
            times = 0
            if row + 4 > 6:
                times = 0
                break
            for col in range(7):
                if col + 4 > 7:
                    times = 0
                    break
                piece = self.board[row][col]
                if piece == ':black_large_square:':
                    times = 0
                    break
                for tries in range(4):
                    try:
                        prow = row+tries
                        pcol = col+tries
                        if piece == self.board[prow][pcol]:
                            times += 1
                        else:
                            times = 0
                            break
                        if times == 4:
                            return True
                    except:
                        break
                    
        # diagonal up
        for row in range(5, -1, -1):
            piece = ''
            times = 0
            if row - 4 < -1:
                times = 0
                break
            for col in range(7):
                if col + 4 > 7:
                    times = 0
                    break
                piece = self.board[row][col]
                if piece == ':black_large_square:':
                    times = 0
                    break
                for tries in range(4):
                    try:
                        prow = row-tries
                        pcol = col+tries
                        if piece == self.board[prow][pcol]:
                            times += 1
                        else:
                            times = 0
                            break
                        if times == 4:
                            return True
                    except:
                        break
        return False
        
    
    def draw(self) -> bool:
        for i in self.positions:
            if i != 0:
                return False
        return True
    