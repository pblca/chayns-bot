import io

import discord
from discord import File
from discord.ext.commands import Context


class CommandHandler:

    def __init__(self, bot, cache):
        self.bot = bot
        self.cache: dict = cache

    def initialize(self):

        @self.bot.command(name='snap')
        async def snap(ctx: Context, channel: discord.TextChannel = None, length: int = 200):
            messages = await channel.history(limit=length).flatten()
            mr = []
            for m in messages:
                mr.append("{} : {} : {}".format(m.created_at, m.author.name, m.content))

            mr.reverse()
            txt = io.StringIO("\n".join(mr))
            await ctx.author.send(file=File(fp=txt, filename="{}-{}.txt".format(channel, ctx.message.created_at)))

        @self.bot.command(name='bing')
        async def snap(ctx: Context):
            await ctx.channel.send("bong")

        @self.bot.command(name='cache')
        async def cache(ctx: Context, key, val):
            self.cache[key] = val

        @self.bot.command(name='showcache')
        async def showcache(ctx: Context):
            await ctx.channel.send(self.cache)

        @self.bot.command(name='mirror')
        async def mirror(ctx: Context):
            if 'mirror_cache' not in self.cache.keys():
                self.cache['mirror_cache']: dict = {ctx.message.channel.id: ctx.message.channel_mentions[0].id}
            else:
                self.cache['mirror_cache'][ctx.message.channel.id] = ctx.message.channel_mentions[0].id
