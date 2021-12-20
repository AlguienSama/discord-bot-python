from discord.ext.commands import Context
from discord import Guild, Member
from utils.responses.Embed import Embed


async def server(ctx: Context):
    guild: Guild = ctx.guild
    owner: Member = await guild.fetch_member(guild.owner_id)

    embed = Embed(title=guild.name, thumbnail=guild.icon_url, image=guild.banner_url, color=0xFF6837)
    embed.add_field(title='ID', desc=guild.id, inline=False)
    embed.add_field(title='Fecha de Creación', desc=guild.created_at, inline=True)
    embed.add_field(title='Propietario/a', desc=str(owner), inline=True)
    embed.add_field(title='Miembros', desc=str(guild.member_count), inline=True)
    embed.add_field(title='Canales de Texto', desc=str(len(guild.text_channels)), inline=True)
    embed.add_field(title='Canales de Voz', desc=str(len(guild.voice_channels)), inline=True)
    embed.add_field(title='Roles', desc=str(len(guild.roles)), inline=True)
    embed.add_field(title='Emoticonos', desc=str(len(guild.emojis)), inline=True)
    #  embed.add_field(title='Pegatinas', desc=str(len(guild.stickers)), inline=True)

    await ctx.send(embed=embed.get_embed())