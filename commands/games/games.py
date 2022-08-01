from discord.ext.commands import *
from commands.games.commands.connect_4 import conenct_4
from commands.games.commands.oj_card import oj_card
from commands.games.commands.oj_game import oj_game
from commands.games.commands.tic_tac_toe import tic_tac_toe
from commands.games.commands.battle_royale import BattleRoyale


class Games(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='tic_tac_toe', aliases=['3raya', '3'])
    async def _tic_tac_toe(self, ctx: Context):
        """ """
        return await tic_tac_toe(self.bot, ctx=ctx)
    
    @command(name='connect4', aliases=['4raya', '4'])
    async def _connect_4(self, ctx: Context):
        """"""
        return await conenct_4(self.bot, ctx)
    
    @command(name='br')
    async def _join_br(self, ctx: Context, name:str=None, image:str=None):
        """ """
        return await BattleRoyale.join(ctx, name, image)
    
    @command(name='oj')
    async def _oj_game(self, ctx: Context):
        """ """
        return await oj_game(ctx)

    @command(name='ojcard')
    async def _oj_card(self, ctx: Context):
        """ """
        return await oj_card(ctx)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Games(bot))
