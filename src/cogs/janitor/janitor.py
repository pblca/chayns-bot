
import os
import time
from collections import deque

import discord
from discord.ext import commands
from discord.ext.commands import Context, bot
from discord import app_commands, Interaction

from dotenv import load_dotenv
from data.cache import cache
load_dotenv()


class Janitor(commands.Cog):

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if 'janitor_cache' in cache.keys() and message.channel.id in cache['janitor_cache'].keys():
            current_cache = cache['janitor_cache'][message.channel.id]
            current_cache['messages'].append(message.id)
            if len(current_cache['messages']) > current_cache['limit']:
                msg: discord.Message = await message.channel.fetch_message(current_cache['messages'].popleft())
                await msg.delete()

    @app_commands.command(name="janitor", description="Enforces a set limit of message after command execution")
    @app_commands.guilds(int(int(os.getenv('TEST_GUILD'))))
    async def janitor(self, interaction: Interaction, limit: int = 200):
        if 'janitor_cache' not in cache.keys():
            cache['janitor_cache']: dict = {interaction.channel_id: {'limit': limit, 'messages': deque()}}
        else:
            cache['janitor_cache'][interaction.channel_id] = {'limit': limit, 'messages': deque()}
        
        await interaction.response.send_message("Janitor active.")
        time.sleep(2)
        await interaction.delete_original_message()


async def setup(bot: commands.Bot):
    await bot.add_cog(Janitor(bot))
