import io
import os
from collections import deque

import discord
from discord.ext import commands
from discord import app_commands, File
from dotenv import load_dotenv

load_dotenv()


class Snap(commands.Cog):

    def __init__(self, _bot: commands.Bot):
        self.bot: commands.Bot = _bot

    @app_commands.command(name='snap', description='Snapshot a text channel')
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def snap(self, interaction: discord.Interaction, channel: discord.TextChannel = None, length: int = 200):
        messages = deque()

        async for message in channel.history(limit=length):
            messages.appendleft(f"{message.created_at} : {message.author.name} : {message.content}")

        txt = io.StringIO("\n".join(messages))
        await interaction.user.send(file=File(fp=txt, filename=f"{channel}-{interaction.created_at}.txt"))


async def setup(_bot: commands.Bot):
    await _bot.add_cog(Snap(_bot))
