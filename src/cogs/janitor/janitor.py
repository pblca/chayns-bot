import os
import time
from collections import deque

import discord
from discord.ext import commands
from discord import app_commands, Interaction

from dotenv import load_dotenv
from data.cache import cache

load_dotenv()


class Janitor(commands.Cog):

    def __init__(self, _bot: discord.ext.commands.Bot):
        self.bot: commands.Bot = _bot

    @classmethod
    @commands.Cog.listener()
    async def on_message(cls, message: discord.Message):
        if 'janitor_cache' in cache and message.channel.id in cache['janitor_cache']:
            current_cache = cache['janitor_cache'][message.channel.id]
            current_cache['messages'].append(message.id)  # replace this with messsage_count
            if len(current_cache['messages']) > current_cache['limit']:
                for _ in range(current_cache['frequency']):
                    current_cache['messages'].popleft()  # likely don't need to store these ids in cache
                await message.channel.purge(limit=current_cache['frequency'], check=lambda x: True)

    @classmethod
    @app_commands.command(name="janitor", description="Enforces a set limit of message after command execution")
    @app_commands.guilds(int(int(os.getenv('TEST_GUILD'))))
    async def janitor(cls, interaction: Interaction, limit: int = 200, frequency: int = 5):
        if 'janitor_cache' not in cache:
            cache['janitor_cache']: dict = {
                interaction.channel_id: {'limit': limit, 'frequency': frequency, 'messages': deque()}}
        else:
            cache['janitor_cache'][interaction.channel_id] = {'limit': limit, 'frequency': frequency,
                                                              'messages': deque()}

        await interaction.response.send_message("Janitor active.")
        time.sleep(2)
        await interaction.delete_original_message()


async def setup(_bot: commands.Bot):
    await _bot.add_cog(Janitor(_bot))
