import io
import os

import discord
from discord import File, app_commands
from discord.ext.commands import Context, Greedy
from discord.ext import commands


class CommandHandler:

    def __init__(self, bot):
        self.bot: commands.Bot = bot

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
