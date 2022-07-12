from discord import User
from discord.ext.commands import Context
from utils.ddbb.games import br_save_player

global games
games = {}

br_senteces = [
    {
        "id": 0,
        "users": 1,
        "deaths": 0,
        "text": ""
    }
]


class Player:
    def __init__(self, user:User=None, name:str=None, image:str=None) -> None:
        if user is not None:
            self.id = user.id
            self.name = name if name is not None else user.display_name
            self.image = image if image is not None else f'https://cdn.discordapp.com{user.avatar_url._url}'
            self.is_death = False
        else:
            # TODO: Default data
            pass
        pass

    def death(self, reason: str):
        self.is_death = reason
    
    async def save(self, server):
        await br_save_player(server, self)
        pass

class BattleRoyale:
    def __init__(self) -> None:
        self.players = []
        self.alive = []
        self.deaths = []
        pass

    def prepare_game(self, guild, channel, admin):
        pass

    @staticmethod
    async def join(ctx: Context, name=None, image=None):
        player = Player(ctx.author, name, image)
        await player.save(ctx.guild.id)
        print("funciona")