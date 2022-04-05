import json

import discord
from discord.ext import commands

from src.utils.connectors import r
from src.utils.misc import str2int


class MirrorUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        r.set('mirror_update_cache', json.dumps({}))

    #@commands.Cog.listener()
    #async def on_message(self, message: discord.Message):
    #    mapping = json.loads(r.get('mirror_cache'), object_hook=str2int)

    #    match mapping:
    #       case {message.channel.id: mirror_channel_id }:
    #           self.bot.get_guild(mirror_channel_id).fetch


async def setup(bot: commands.Bot):
    await bot.add_cog(MirrorUpdate(bot))
