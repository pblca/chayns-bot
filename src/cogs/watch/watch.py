
import discord
from discord.ext import commands
from discord.ext.commands import Context


class Watch(commands.Cog):

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot: commands.bot = bot

    @commands.command(name="watch")
    async def watch(self, ctx: Context):
        await ctx.channel.send("hi :)")

def setup(bot):
    bot.add_cog(Watch(bot))
