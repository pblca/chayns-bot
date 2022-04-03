
import os
import time
from collections import deque

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands, Interaction

from dotenv import load_dotenv
load_dotenv()

class Warn(commands.Cog):

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name='warn', description='Log a warn of a member with a reason')
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def warn(self, interaction: Interaction, user: discord.User, reason: str):
        if 'warns_cache' not in self.bot.cache.keys():
            self.bot.cache['warns_cache'] = {user.id: [(reason, interaction.created_at)]}
        else:
            if user.id in self.bot.cache['warns_cache'].keys():
                self.bot.cache['warns_cache'][user.id].append((reason, interaction.created_at))
            else:
                self.bot.cache['warns_cache'][user.id] = [(reason, interaction.created_at)]
        await interaction.response.send_message(f'{user.name}#{user.discriminator} has been warned.')
    @app_commands.command(name='view-warns', description='View a user\'s warns')
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def view_warns(self, interaction: Interaction, user: discord.User):
        if 'warns_cache' not in self.bot.cache.keys() or user.id not in self.bot.cache['warns_cache'].keys():
            await interaction.response.send_message("That user has never no warns")
            time.sleep(1)
            await interaction.delete_original_message()
            return
        await interaction.response.send_message(embeds = [discord.Embed(
            title=f'WARN {i+1}',
            colour=0x377FF5,
            description=f'Reason: {reason[0]}'
            ).set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar.url).set_footer(text=reason[1]) for i, reason in enumerate(self.bot.cache['warns_cache'][user.id])])

async def setup(bot):
    await bot.add_cog(Warn(bot))


