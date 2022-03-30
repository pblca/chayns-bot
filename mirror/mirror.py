import discord
from discord.ext import commands
class Mirror(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, ctx, message: discord.Message):
        if 'mirror_cache' in self.cache.keys() and message.channel.id in self.cache['mirror_cache'].keys():
            mirror_channel_id = self.cache['mirror_cache'][message.channel.id]
            await message.guild.get_channel(mirror_channel_id).send(
                f"[{message.created_at}] [{message.channel.name}] \n[{message.author.name}] : {message.content}")

