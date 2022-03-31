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
