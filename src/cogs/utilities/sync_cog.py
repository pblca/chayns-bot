import io
import json
import os
from typing import Optional, Literal
import discord
from discord.ext import commands
from discord import app_commands, Interaction, File
from dotenv import load_dotenv

from data.cache import cache

from data.cache import cache
from src.utils.connectors import r
from src.utils.delete_view import DeleteView
from src.utils.misc import str2int

load_dotenv()


class Sync(commands.Cog):

    def __init__(self, _bot: commands.Bot):
        self.bot: commands.Bot = _bot

    @app_commands.command(name='sync', description='synchronize command database')
    @app_commands.guilds(int(int(os.getenv('TEST_GUILD'))))
    async def sync(self, interaction: Interaction, spec: Optional[Literal["~"]] = None) -> None:
        guilds = self.bot.guilds
        if not guilds:
            if spec == "~":
                fmt = await self.bot.tree.sync(guild=discord.Object(interaction.guild.id))
            else:
                fmt = await self.bot.tree.sync()

            await interaction.response.send_message(
                f"Synced {len(fmt)} commands {'globally' if spec is not None else 'to the current guild.'}"
            )
            return

        assert guilds is not None
        fmt = 0
        for guild in guilds:
            try:
                await self.bot.tree.sync(guild=discord.Object(id=guild.id))
            except discord.HTTPException as ex:
                print(ex)
            else:
                fmt += 1

        await interaction.response.send_message(f"Synced the tree to {fmt}/{len(guilds)} guilds.")


async def setup(_bot: commands.Bot):
    await _bot.add_cog(Sync(_bot))
