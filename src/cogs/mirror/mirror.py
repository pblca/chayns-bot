import os
import time

from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from data.cache import cache
from dotenv import load_dotenv


load_dotenv()


class Mirror(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if 'mirror_cache' in cache.keys() and message.channel.id in cache['mirror_cache'].keys():
            mirror_channel_id = cache['mirror_cache'][message.channel.id]
            await message.guild.get_channel(mirror_channel_id).send(
                f"[{message.created_at}] [{message.channel.name}] \n[{message.author.name}] : {message.content}")

    # This is mainly for testing
    @app_commands.command(name='cache')
    async def cache(self, interaction: discord.Interaction, key: Optional[str], val: Optional[str]):
        if key:
            if key not in cache.keys():
                return
            if val:
                cache[key] = ' '.join(str(arg) for arg in val[1:])
            else:
                await interaction.response.send_message(cache[key])
        else:
            await interaction.response.send_message(cache)
        
    @app_commands.command(name='mirror')
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def mirror(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if 'mirror_cache' not in cache.keys():
            cache['mirror_cache']: dict = {interaction.channel_id: channel.id}
        else:
            cache['mirror_cache'][interaction.channel_id] = channel.id
        await interaction.response.send_message(f'Mirroring {interaction.channel_id} into {channel.mention}!')
        time.sleep(2)
        await interaction.delete_original_message()


async def setup(bot):
    await bot.add_cog(Mirror(bot))
