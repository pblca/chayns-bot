from linecache import cache
import discord
from discord.ext import commands
from discord.ext.commands import Context


class Mirror(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if 'mirror_cache' in self.bot.cache.keys() and message.channel.id in self.bot.cache['mirror_cache'].keys():
            mirror_channel_id = self.bot.cache['mirror_cache'][message.channel.id]
            await message.guild.get_channel(mirror_channel_id).send(
                f"[{message.created_at}] [{message.channel.name}] \n[{message.author.name}] : {message.content}")

    # This is mainly for testing
    @commands.command(name='cache')
    async def cache(self, ctx: Context, *args):
        if len(args) == 0:
            await ctx.channel.send(self.bot.cache)
        elif len(args) == 1:
            if args[0] in self.bot.cache.keys():
                await ctx.channel.send(self.bot.cache[args[0]])
        else:
            self.bot.cache[args[0]] = ' '.join(str(arg) for arg in args[1:])

    @commands.command(name='mirror')
    async def mirror(self, ctx: Context):
        if 'mirror_cache' not in self.bot.cache.keys():
            self.bot.cache['mirror_cache']: dict = {ctx.message.channel.id: ctx.message.channel_mentions[0].id}
        else:
            self.bot.cache['mirror_cache'][ctx.message.channel.id] = ctx.message.channel_mentions[0].id

def setup(bot):
    bot.add_cog(Mirror(bot))
