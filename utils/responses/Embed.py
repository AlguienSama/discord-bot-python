from __future__ import annotations

import discord


class Embed:
    """Constructor de embeds"""
    title: str = None
    color: int = None
    description: str = None
    image: str = None

    def __init__(self, user: discord.User = None, title: str = None, description: str = None, color: int = None,
                 image: str = None, thumbnail: str = None):
        self.embed = discord.Embed(description=description)
        self.embed.set_footer(text="IT Crowd", icon_url="https://cdn.discordapp.com/emojis/562075100116156418.png")
        if user:
            self.embed.set_author(name=user.display_name, icon_url=user.avatar.url)
        if title:
            self.embed.title = title
        if description:
            self.embed.description = description
        else:
            self.embed.description = '_ _'
        if color:
            self.embed.colour = color
        if image:
            self.embed.set_image(url=image)
        if thumbnail:
            self.embed.set_thumbnail(url=thumbnail)

    def success(self) -> Embed:
        self.embed.colour = 0x22E000
        return self

    def failure(self) -> Embed:
        self.embed.colour = 0xAA0000
        return self

    def warn(self) -> Embed:
        self.embed.colour = 0xFFB200
        return self
    
    def roulette(self) -> Embed:
        self.embed.colour = 0xCBFF16

    def economy(self) -> Embed:
        self.embed.colour = 0xFFDB26
        return self

    def add_field(self, title: str, desc: str, inline: bool = False) -> Embed:
        self.embed.add_field(name=title, value=desc, inline=inline)
        return self
    
    def set_author(self, name, icon_url) -> Embed:
        self.embed.set_author(name=name, icon_url=icon_url)
        return self
    
    def set_image(self, image) -> Embed:
        self.embed.set_image(url=image)

    def get_embed(self) -> discord.Embed:
        if self.title:
            self.embed.title = self.title
        if self.description:
            self.embed.description = self.description
        if self.color:
            self.embed.colour = self.color
        return self.embed