from discord.ext.commands import Context, Bot, UserConverter
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from utils.responses.Embed import Embed

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('utils/ddbb/keys/excel-haikoins.json', scope)
client = gspread.authorize(creds)


async def get_haikoin(ctx: Context, user=None):
    sh = client.open_by_key('1B8JpepOxGVkebwLuNRlPsXZ23hrUEjSM_nMHKbad0ts')
    worksheet = sh.get_worksheet(0)

    try:
        user = await UserConverter().convert(ctx, user)
    except:
        user = ctx.author

    cell = worksheet.find(str(user.id))

    if cell is None:
        embed = Embed(user=user, description='Balance 💰') \
            .add_field('Haikoins:', '0', True) \
            .economy()
    else:
        value = worksheet.cell(cell.row, 6).value
        embed = Embed(user=user, description='Balance 💰')\
            .add_field('Haikoins:', f'{value}', True)\
            .economy()

    await ctx.send(embed=embed.get_embed())
