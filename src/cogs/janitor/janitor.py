from collections import deque

import discord
from discord.ext import commands
from discord.ext.commands import Context


class Janitor(commands.Cog):

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if 'janitor_cache' in self.bot.cache.keys() and message.channel.id in self.bot.cache['janitor_cache'].keys():
            current_cache = self.bot.cache['janitor_cache'][message.channel.id]
            current_cache['messages'].append(message.id)
            if len(current_cache['messages']) > current_cache['limit']:
                msg: discord.Message = await message.channel.fetch_message(current_cache['messages'].popleft())
                await msg.delete()

    @commands.command(name='janitor')
    async def janitor(self, ctx: Context, limit=200):
        if 'janitor_cache' not in self.bot.cache.keys():
            self.bot.cache['janitor_cache']: dict = {ctx.message.channel.id: {'limit': limit, 'messages': deque()}}
        else:
            self.bot.cache['janitor_cache'][ctx.message.channel.id] = {'limit': limit, 'messages': deque()}

def setup(bot):
    bot.add_cog(Janitor(bot))