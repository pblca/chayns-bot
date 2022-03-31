from collections import deque

import discord
from discord.ext import commands
from discord.ext.commands import Context


class Janitor(commands.Cog):

    def __init__(self, bot: discord.ext.commands.Bot, cache: dict):
        self.bot: commands.Bot = bot
        self.cache: dict = cache

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if 'janitor_cache' in self.cache.keys() and message.channel.id in self.cache['janitor_cache'].keys():
            current_cache = self.cache['janitor_cache'][message.channel.id]
            current_cache['messages'].append(message.id)
            if len(current_cache['messages']) > current_cache['limit']:
                msg: discord.Message = await message.channel.fetch_message(current_cache['messages'].popleft())
                await msg.delete()

    @commands.command(name='janitor')
    async def janitor(self, ctx: Context, limit=200):
        if 'janitor_cache' not in self.cache.keys():
            self.cache['janitor_cache']: dict = {ctx.message.channel.id: {'limit': limit, 'messages': deque()}}
        else:
            self.cache['janitor_cache'][ctx.message.channel.id] = {'limit': limit, 'messages': deque()}
