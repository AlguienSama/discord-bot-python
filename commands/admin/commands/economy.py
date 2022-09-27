import discord
from discord.ext.commands import Context, UserConverter
from disputils import BotConfirmation
from utils.errors import MoneyError
from utils.logs.economy import lose_money, win_money
from utils.responses.Embed import Embed
from utils.ddbb.economy import *


class Buttons(discord.ui.View):
    def __init__(self, ctx: Context, user: discord.User, money: int, embed: Embed, is_add: bool):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.user = user
        self.money = money
        self.embed = embed
        self.is_add = is_add
    
    @discord.ui.button(label='Aceptar', style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        msg = ''
        if self.is_add:
            await win_money(self.ctx, self.user, self.money, f'Add money by {self.ctx.author.id}')
            msg = f'{int(self.money):,} 💰 **entregado** correctamente al usuario <@{self.user.id}>'
            self.embed.success()
        else:
            await lose_money(self.ctx, self.user, self.money, f'Add money by {self.ctx.author.id}')
            msg = f'{int(self.money):,} 💰 **quitado** correctamente al usuario <@{self.user.id}>'
            self.embed.success()
        self.embed.description = msg
        await interaction.response.edit_message(embed=self.embed.get_embed(), view=None)
        
    @discord.ui.button(label='Rechazar', style=discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.description = 'Operación cancelada!'
        self.embed.failure()
        await interaction.response.edit_message(embed=self.embed.get_embed(), view=None)


async def add_money(ctx: Context, user: discord.User, money: int):
    try:
        money = int(money)
        if money < 1:
            raise
    except:
        raise MoneyError(min=1)
    embed = Embed(title='Entrega de dinero', description=f'Seguro que quieres **entregar** {int(money):,} 💰 a {user.mention}?', user=ctx.author).warn()
    await ctx.channel.send(embed=embed.get_embed(), view=Buttons(ctx, user, money, embed, True))



async def remove_money(ctx: Context, user, money: int):
    try:
        money = int(money)
        if money < 1:
            raise
    except:
        raise MoneyError(min=1)
    embed = Embed(title='Entrega de dinero', description=f'Seguro que **quitar** dar {int(money):,} 💰 a {user.mention}?', user=ctx.author).warn()
    await ctx.channel.send(embed=embed.get_embed(), view=Buttons(ctx, user, money, embed, False))
