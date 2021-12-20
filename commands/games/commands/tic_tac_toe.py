from discord.ext.commands import *
from discord import User
from utils.ddbb.games import start_tic_tac_toe
import asyncio
import re
from utils.errors import CustomError
from utils.responses.Embed import Embed


async def tic_tac_toe(bot: Bot, ctx: Context):
    await ctx.channel.send(f'Esperando que el oponente acepte la partida `{ctx.prefix}accept` (60 segundos)')

    def check(m):
        return m.content == f'{ctx.prefix}accept' and m.channel == ctx.channel and m.author.id != ctx.author.id

    user = None
    try:
        user = await bot.wait_for('message', check=check, timeout=60.0, )
    except asyncio.TimeoutError:
        await ctx.channel.send('Time Out ')
        raise CustomError('No puede jugar en soledad, lo siento.')
    else:
        message = await ctx.channel.send(
            'Recuerda que debes de enviar el número correspondiente a la casilla donde quieres '
            'poner la ficha...')

    user = user.author
    if user is None:
        raise CustomError('Invalid player')

    [cross, circle] = await start_tic_tac_toe(ctx.guild.id)

    game = TicTacToe(bot, ctx, message, ctx.author, user, cross, circle)
    await game.start()


board_positions = {
    '1': [0, 0],
    '2': [0, 1],
    '3': [0, 2],
    '4': [1, 0],
    '5': [1, 1],
    '6': [1, 2],
    '7': [2, 0],
    '8': [2, 1],
    '9': [2, 2],
}
pattern = re.compile('^[1-9]$')


class TicTacToe:
    def __init__(self, bot: Bot, ctx: Context, message, player1: User, player2: User, cross: str = ':x:',
                 circle: str = ':o:'):
        self.bot = bot
        self.ctx = ctx
        self.board = [[':one:', ':two:', ':three:'],
                      [':four:', ':five:', ':six:'],
                      [':seven:', ':eight:', ':nine:']]
        self.channel = ctx.channel
        self.player1 = player1
        self.player2 = player2
        self.piece1 = cross
        self.piece2 = circle
        self.turn = 1
        self.game = 1
        self.message = message

    def check_turn(self, m):
        try:
            content = self.board[board_positions[m.content][0]][board_positions[m.content][1]]
            return pattern.match(m.content) is not None and \
                   m.channel == self.channel and \
                   m.author.id == (self.player1.id if self.turn == 1 else self.player2.id) and \
                   (content != self.piece1 and content != self.piece2)
        except:
            return False

    async def start(self):
        while self.game == 1:
            player = self.player1 if self.turn == 1 else self.player2
            piece = self.piece1 if self.turn == 1 else self.piece2
            await self.msg_send(player, piece)
            try:
                content = await self.bot.wait_for('message', check=self.check_turn, timeout=15.0)
                self.board[board_positions[content.content][0]][board_positions[content.content][1]] = piece
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
            msg += " | ".join(row) + "\n"
        return msg

    async def msg_send(self, player, piece):
        msg = f'Turno de {player} {piece}\n' \
              f'Tiempo límite de 15 segundos para hacer tu movimiento'
        msg += f'\n{self.msg_board()}'
        embed = Embed().add_field('3 en Raya', msg)
        await self.message.edit(embed=embed.get_embed())

    async def msg_draw(self):
        msg = f'!!EMPATE!!\n'
        msg += f'\n{self.msg_board()}'
        embed = Embed().add_field('3 en Raya', msg)
        await self.message.edit(embed=embed.get_embed())

    async def msg_win(self, player, piece):
        msg = f'!!VICTORIA de {player} {piece}!!\n'
        msg += f'\n{self.msg_board()}'
        embed = Embed().add_field('3 en Raya', msg)
        await self.message.edit(embed=embed.get_embed())

    def win(self) -> bool:
        # Check Rows
        for row in self.board:
            if len(set(row)) == 1:
                return True

        # Check Cols
        for row in range(len(self.board[0])):
            nums = []
            for col in range(len(self.board[0])):
                nums.append(self.board[col - 1][row - 1])
            if len(set(nums)) == 1:
                return True

        # Check Diagonals
        if self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2]:
            return True
        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            return True

        return False

    def draw(self) -> bool:
        # Check Rows
        draw = True
        for row in self.board:
            for num in row:
                if not (num == self.piece1 or num == self.piece2):
                    return False
        return True
