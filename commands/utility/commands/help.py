from typing import Any
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Command, Context

from utils.responses.Embed import Embed


class CommandSelect(discord.ui.Select):
    def __init__(self, *, help_view, commands: object) -> None:
        options = []
        for command in commands:
            discord.SelectOption(label=command.name, value='main')
        super().__init__(placeholder='Selecciona un comando', options=options, min_values=1, max_values=1)


class CategorySelect(discord.ui.Select):
    def __init__(self, help_view, commands: object) -> None:
        self.help_view = help_view
        options = [
            discord.SelectOption(label='Menú Principal', value='main')
        ]
        for command in commands:
            key = list(command.keys())[0]
            options.append(discord.SelectOption(label=key, description=f'{command[key][:50]}...', value=key))
        super().__init__(placeholder='Selecciona una categoría', min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.help_view.help.get_embed(self.help_view.category))


class HelpView(discord.ui.View):
    def __init__(self, help, commands: object, timeout = 60) -> None:
        super().__init__(timeout=timeout)
        self.help = help
        self.commands = commands
        self.select = CategorySelect(self, self.commands)
        self.add_item(self.select)
        self.category = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        self.category = self.select.values[0]
        return True
         

class Help(commands.HelpCommand):
    def __init__(self, **options: Any) -> None:
        self.commands = []
        super().__init__(**options)
    # Without args
    async def send_bot_help(self, mapping, /) -> None:
        print('send_bot_help')
        self.get_command_list(mapping)
        await self.get_destination().send(embed=self.get_embed(), view=HelpView(self, self.commands))
        return await super().send_bot_help(mapping)
    
    # With command
    async def send_command_help(self, command, /) -> None:
        print('send_command_help')
        return await super().send_command_help(command)
    
    # With cog
    async def send_cog_help(self, cog: Cog, /) -> None:
        print('send_cog_help')
        print('cog', cog)
        self.get_command_list(self.get_bot_mapping())
        await self.get_destination().send(embed=self.get_embed(Cog), view=HelpView(self, self.commands))
        return await super().send_cog_help(cog)
    
    # Error message
    async def send_error_message(self, error: Exception) -> None:
        print('send_error_message', error)
        print('type(error)', type(error))
        if error.startswith('No command called "'):
            await self.send_bot_help(self.get_bot_mapping())
        return await super().send_error_message(error)
    
    async def on_help_command_error(self, ctx, error, /) -> None:
        print('on_help_command_error', type(error).__name__)
        return await super().on_help_command_error(ctx, error)
    
    
    def get_command_list(self, mapping):
        for cog in mapping:
            if cog == None:
                continue
            command_list = ''
            for c in cog.get_commands():
                command_list += f'{c.name}, '
            self.commands.append({cog.qualified_name: command_list})
    
    def get_cog_commands(self, category: str):
        commands = self.get_bot_mapping()
        for cog in commands:
            if cog == None:
                continue
            if cog.qualified_name == category:
                return cog.get_commands()
    
    
    def get_embed(self, category: str = None) -> discord.Embed:
        embed = Embed(title=f'Ayuda {f"- {category}" if category is not None else ""}', color=0x00ff00)
        if category is None:
            embed.description = 'Aquí encontrarás todos los comandos disponibles!'
        else:
            text = ''
            commands = self.get_cog_commands(category)
            for command in commands:
                if command.description:
                    text += f'{command.name}: `{command.description}`\n'
                else:
                    text += f'{command.name}\n'
            embed.description = text
        return embed.get_embed()
    
    def get_destination(self):
        return self.context.author