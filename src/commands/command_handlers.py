import io

import discord
from discord import File
from discord.ext.commands import Context
from discord.ext import commands


class CommandHandler:

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    def initialize(self):
        @self.bot.command(name='snap')
        async def snap(ctx: Context, channel: discord.TextChannel = None, length: int = 200):
            messages = await channel.history(limit=length).flatten()
            message_return = []
            for message in messages:
                message_return.append(f"{message.created_at} : {message.author.name} : {message.content}")

            message_return.reverse()
            txt = io.StringIO("\n".join(message_return))
            await ctx.author.send(file=File(fp=txt, filename=f"{channel}-{ctx.message.created_at}.txt"))

        @self.bot.command(name='bing')
        async def bing(ctx: Context):
            await ctx.channel.send("bong")
