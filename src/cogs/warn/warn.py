
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
        pass

async def setup(bot):
    await bot.add_cog(Warn(bot))


