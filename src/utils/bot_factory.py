import asyncio
import os
from re import split as regsplit
import discord
from discord.ext import commands

from src.events.event_handlers import EventHandler
from db.setup import init
from data.cache import cache


class BotFactory:

    def __init__(self, prefix: str):
        intents = discord.Intents().all()
        self.engine = init()

        self.bot = commands.Bot(command_prefix=prefix, intents=intents)

        # I really don't like pinning attributes like this.
        self.bot.engine = self.engine

        cache['guild_ids'] = [guild.id for guild in self.bot.guilds]
        self.event_handlers = EventHandler(self.bot)

    def start(self):
        initial_extensions = []
        # Go fetch py files in the nested directories within src/cogs
        for root, _, filenames in os.walk('src/cogs'):
            for filename in filenames:
                if filename.endswith(".py"):
                    directory = regsplit(r'[/\\]', root)[-1]
                    cogs_directory = directory == 'cogs'

                    # because we're in utils here we need to up a directory so to load the janitor cog from
                    # src/cogs/janitor/janitor_cog.py, it needs to look like ..cogs.janitor.janitor_cog
                    extension_prefix = "..cogs" if cogs_directory else f"..cogs.{directory}"
                    if f'{directory}_cog' == f'{filename[:-3]}':
                        initial_extensions.append(f"{extension_prefix}.{filename[:-3]}")

        # Here we load our extensions(cogs) listed above in [initial_extensions].
        for extension in initial_extensions:
            asyncio.run(self.bot.load_extension(name=extension, package=__package__))

        self.event_handlers.initialize()
        self.bot.run(os.getenv('BOT_KEY'))
