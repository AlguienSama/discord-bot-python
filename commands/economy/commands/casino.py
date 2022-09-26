import asyncio
import random
import threading
import time
import discord
from discord.ext.commands import Context, Bot
from utils.logs.economy import lose_money, win_money
from utils.ddbb.economy import check_bal
from utils.errors import CustomError, MoneyError
from utils.responses.Embed import Embed


numbers = []
for i in range(37):
    numbers.append(str(i))
parities = {'even': ['par', 'even'], 'odd': ['impar', 'odd']}
halfs = {'1-18': ['1-18'], '19-36': ['19-36']}
trios = {'1st': ['1st', '1-12'], '2nd': ['2nd', '13-24'], '3rd': ['3rd', '25-36']}
rows = {'r1': ['r1', 'f1'], 'r2': ['r2', 'f2'], 'r3': ['r3', 'f3']}
colors = {'red': ['red', 'rojo'], 'black': ['black', 'negro'], 'green': ['green', 'verde']}

async def flip(ctx: Context, money: int):
    res = random.randint(0, 1)
    if money < 1:
        raise MoneyError(min=1)

    await check_bal(ctx.guild.id, ctx.author.id, money)

    embed = Embed(title='FLIP GAME')

    await win(ctx, ctx.author, money, 'Flip')

    if res == 0:
        money *= -1
        embed.description = f'Has perdido `{abs(money)}` haikoins!!'
        embed.failure()
    else:
        embed.description = f'Has ganado `{abs(money)}` haikoins!!'
        embed.success()
    await update_bal(ctx.guild.id, ctx.author.id, money)

    await ctx.send(embed=embed.get_embed())


class Roulette(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.bets = []
        self.bets.append(args[0])
        self.bot: Bot = args[1]
        self.guild: discord.Guild = args[2]
        self.channel: discord.TextChannel = args[3]
        self.timer = threading.Event()
        self.time = 5
        self.final_time = int(round(time.time())) + self.time
    
    def run(self):
        self.timer.wait(self.time)
        asyncio.run(self.game_start())
        print(self.bets)
    
    def stop_timer(self):
        self.timer.set()
    
    def time_left(self):
        return (self.final_time - int(round(time.time())))
    
    def add_bet(self, bet):
        self.bets.append(bet)
    
    async def game_start(self):
        print('starting game')
        channel = self.bot.get_channel(self.channel.id)
        await channel.send('Pito')


async def join_roulette(bot: Bot, ctx: Context, money: int, args):
    try:
        money = int(money)
        if money < 1:
            raise MoneyError(min=1)
    except:
        raise CustomError('Invalid Ammount')

    if not args:
        raise CustomError('A que quieres apostar')
    
    bet = {'user': ctx.author.id, 'ammount': money, 'total_ammount': 0, 'v': 0, 'bets': {'num': [], 'par': [], 'half': [], 'trio': [], 'row': [], 'color': []}}
    def check_bet(arg, vals, name):
        for val in vals:
            if val == arg:
                bet['bets'][name].append(val)
                bet['v']+=1
                return True
            try:
                for d in vals[val]:
                    if d == arg:
                        bet['bets'][name].append(val)
                        bet['v']+=1
                        return True
            except:
                pass
    for arg in args:
        if check_bet(arg, numbers, 'num'):
            continue
        if check_bet(arg, parities, 'par'):
            continue
        if check_bet(arg, halfs, 'half'):
            continue
        if check_bet(arg, trios, 'trio'):
            continue
        if check_bet(arg, rows, 'row'):
            continue
        if check_bet(arg, colors, 'color'):
            continue
    
    bet['total_ammount'] = bet['ammount']*bet['v']
    #await check_bal(ctx.guild.id, ctx.author.id, bet['total_ammount'])
    #await lose_money(ctx.guild.id, ctx.author.id, bet['total_ammount'], 'Ruleta')
    
    """ for thread in threading.enumerate():
        if thread.name == f'roulette_{ctx.guild.id}':
            exists = True
            thread.add_bet(bet)
            print(f'Time left: {thread.time_left()} seconds')
            if args[4] == 'blu':
                thread.stop_timer()

    if not exists:
        r = Roulette(name=f'roulette_{ctx.guild.id}', args=(bet, bot, ctx.guild, ctx.channel), daemon=True)
        r.start()
        print(f'Starting roulette game in channel {ctx.channel.id}') """
    global games
    
    async def send_message():
        def check_bet(args, vals):
            string = '| '
            for arg in args:
                for val in vals:
                    if str(val) == str(arg):
                        string += f'{str(val)} | '
                    continue
            return string
        
        desc = f"Dinero apostado: **{bet['ammount']}** 💰 \n"
        desc += f"Dinero total: **{bet['total_ammount']}** 💰 \n"
        res = check_bet(bet['bets']['num'], numbers)
        if res != '| ':
            desc += f'Números: **{res}**\n'
        res = check_bet(bet['bets']['par'], parities)
        if res != '| ':
            desc += f'Paridades: **{res}**\n'
        res = check_bet(bet['bets']['half'], halfs)
        if res != '| ':
            desc += f'Mitades: **{res}**\n'
        res = check_bet(bet['bets']['trio'], trios)
        if res != '| ':
            desc += f'Tríos: **{res}**\n'
        res = check_bet(bet['bets']['row'], rows)
        if res != '| ':
            desc += f'Filas: **{res}**\n'
        res = check_bet(bet['bets']['color'], colors)
        if res != '| ':
            desc += f'Colores: **{res}**\n'
        
        embed = Embed(title='Ruleta', user=ctx.author, description=f"**{games[f'{ctx.channel.id}']['time'] - int(round(time.time()))} segundos** restantes")
        embed.warn().add_field(title='Apuestas', desc=desc)
        await ctx.channel.send(embed=embed.get_embed())
        
    try:
        games[f'{ctx.channel.id}']['bets'].append(bet)
        await send_message()
    except:
        games = {}
        games[f'{ctx.channel.id}'] = {'guild': ctx.guild.id, 'channel': ctx.channel.id, 'creator': ctx.author.id, 'time': int(round(time.time())) + 10, 'bets': []}
        games[f'{ctx.channel.id}']['bets'].append(bet)
        await send_message()
        await asyncio.sleep(10)
        game = games[f'{ctx.channel.id}']
        del games[f'{ctx.channel.id}']
        num = random.randint(0, 36)
        par = 'odd' if num % 2 != 0 else 'even' if num != 0 else 0
        half = '19-36' if num > 18 else '1-18' if num != 0 else 0
        trio = '3rd' if num > 24 else '2nd' if num > 12 else '1st' if num != 0 else 0
        row = 'r1' if num % 3 == 1 else 'r2' if num % 3 == 2 else 'r3' if num != 0 else 0
        color = 'red' if num > 0 and num < 11 and num % 2 == 1 or num > 10 and num < 19 and num % 2 == 0 or num > 18 and num < 29 and num % 2 == 1 or num > 28 and num < 37 and num % 2 == 0 else 'black' if num != 0 else 0
        
        wins = {}
        loses = []
        def check_win(arr, val):
            for a in arr:
                if str(a) == str(val):
                    return True
            return False
        
        for bet in game['bets']:
            ammount = 0
            
            if check_win(bet['bets']['num'], num):
                ammount += bet['ammount'] * 36
            if check_win(bet['bets']['par'], par):
                ammount += bet['ammount'] * 2
            if check_win(bet['bets']['half'], half):
                ammount += bet['ammount'] * 2
            if check_win(bet['bets']['trio'], trio):
                ammount += bet['ammount'] * 3
            if check_win(bet['bets']['row'], row):
                ammount += bet['ammount'] * 3
            if check_win(bet['bets']['color'], color):
                ammount += bet['ammount'] * 2
            
            user_id = str(bet['user'])
            if ammount != 0:
                if user_id in wins:
                    wins[user_id] += ammount
                else:
                    wins[user_id] = ammount
            else:
                loses.append(user_id)
        
        ganadores = ''
        for win in wins:
            ganadores += f'**<@{win}> + {wins[win]} 💰**\n'
        if ganadores == '':
            ganadores = 'Nadie ganó'
        
        result = f'**Número {num}**'
        if num != 0:
            result += f'\n{par}, {half}, {trio}, {row}, {color}'
        embed = Embed(title='Ruleta', description=result).success()
        embed.add_field(title='Ganadores', desc=ganadores)
        await ctx.channel.send(embed=embed.get_embed())

