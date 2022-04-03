import io
import json
import os
import time
import discord
from discord.ext import commands
from discord import app_commands, File
from dotenv import load_dotenv

from data.cache import cache

load_dotenv()


class Mirror(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if 'mirror_cache' in cache and message.channel.id in cache['mirror_cache']:
            mirror_channel_id = cache['mirror_cache'][message.channel.id]
            await message.guild.get_channel(mirror_channel_id).send(
                f"[{message.created_at}] [{message.channel.name}] \n[{message.author.name}] : {message.content}")

    # This is mainly for testing
    @app_commands.command(name='get-cache')
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def get_cache(self, interaction: discord.Interaction):
        txt = io.StringIO(json.dumps(cache, indent=2, default=str))
        file = File(fp=txt, filename="ok.txt")
        await interaction.response.send_message(file=file)

    @app_commands.command(name='mirror')
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def mirror(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if 'mirror_cache' not in cache:
            cache['mirror_cache']: dict = {interaction.channel_id: channel.id}
        else:
            cache['mirror_cache'][interaction.channel_id] = channel.id
        await interaction.response.send_message(f'Mirroring {interaction.channel_id} into {channel.mention}!')
        time.sleep(2)
        await interaction.delete_original_message()


async def setup(bot):
    await bot.add_cog(Mirror(bot))
