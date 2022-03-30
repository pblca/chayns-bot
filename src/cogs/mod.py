import io

import discord
import inspect
from discord import File
from discord.ext.commands import Context
from discord.ext import commands


class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='snap')
    async def snap(ctx: Context, channel: discord.TextChannel = None, length: int = 200):
        messages = channel.history(limit=length).flatten()
        mr = []
        for m in messages:
            mr.append("{} : {} : {}".format(m.created_at, m.author.name, m.content))

        mr.reverse()
        txt = io.StringIO("\n".join(mr))
        await ctx.author.send(file=File(fp=txt, filename="{}-{}.txt".format(channel, ctx.message.created_at)))

    @commands.command(name='bing')
    async def snap(ctx: Context):
        await ctx.channel.send("bong")

def setup(bot):
    bot.add_cog(Mod(bot))