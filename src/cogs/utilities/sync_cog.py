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

    # This is mainly for testing
    @app_commands.command(name='get-cache')
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def get_cache(self, interaction: discord.Interaction):
        keys = r.keys('*')
        d = {}
        for x in filter(lambda n: n not in 'redis_test', keys):
            val = r.get(x)
            d[x] = json.loads(val, object_hook=str2int)

        txt = io.StringIO(json.dumps(d, indent=2, default=str))
        file = File(fp=txt, filename="cache.txt")
        await interaction.response.send_message(file=file, view=DeleteView())


async def setup(_bot: commands.Bot):
    await _bot.add_cog(Sync(_bot))
