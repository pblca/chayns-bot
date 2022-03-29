import io
import os

import discord
from discord import File
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!bing'):
        await message.channel.send('bong')

    await bot.process_commands(message)


@bot.command(name='snap')
async def snap(ctx, channel: discord.TextChannel = None, length: int = 200):
    messages = await channel.history(limit=length).flatten()
    mr = []
    for m in messages:
        mr.append("{} : {} : {}".format(m.created_at, m.author.name, m.content))

    mr.reverse()
    txt = io.StringIO("\n".join(mr))
    await ctx.author.send(file=File(fp=txt, filename="{}-{}.txt".format(channel, ctx.message.created_at)))

bot.run(os.getenv('BOT_KEY'))
