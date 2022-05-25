from ast import alias
from discord_slash import SlashCommand
from discord.ext.commands import *
from commands.games.commands.connect_4 import conenct_4
from commands.games.commands.tic_tac_toe import tic_tac_toe
from commands.games.commands.battle_royale import BattleRoyale


class Games(Cog):
    def __init__(self, bot: Bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

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


def setup(bot: Bot) -> None:
    bot.add_cog(Games(bot))
