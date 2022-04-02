import io

import discord
from discord import File
from discord.ext.commands import Context, Greedy
from discord.ext import commands
from typing import Optional, Literal
class CommandHandler:

    def __init__(self, bot):
        self.bot = bot

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
    
        @self.bot.command()
        @commands.is_owner()
        async def sync(ctx: Context, guilds: Greedy[int], spec: Optional[Literal["~"]] = None) -> None:
            if not guilds:
                if spec == "~":
                    fmt = await ctx.bot.tree.sync(guild=ctx.guild)
                else:
                    fmt = await ctx.bot.tree.sync()

                await ctx.send(
                    f"Synced {len(fmt)} commands {'globally' if spec is not None else 'to the current guild.'}"
                )
                return

            assert guilds is not None
            fmt = 0
            for guild in guilds:
                try:
                    await ctx.bot.tree.sync(guild=discord.Object(id=guild))
                except discord.HTTPException as ex:
                    print(ex)
                else:
                    fmt += 1

            await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds.")
        
        @self.bot.command(name='bing')
        async def snap(ctx: Context):
            await ctx.channel.send("bong")
