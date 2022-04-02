import os
import discord
from discord.ext import commands


from src.cogs.mirror.mirror import Mirror
from src.cogs.janitor.janitor import Janitor
from src.commands.command_handlers import CommandHandler
from src.events.event_handlers import EventHandler

from re import split as regsplit

class BotFactory:

    def __init__(self, prefix: str):
        intents = discord.Intents().all()
        self.cache: dict = {}
        self.bot = commands.Bot(command_prefix=prefix, intents=intents)
        self.event_handlers = EventHandler(self.bot)
        self.command_handlers = CommandHandler(self.bot)
        self.bot.cache = self.cache

    def start(self):
        initial_extensions = []
        # Go fetch py files in the nested directories within src/cogs
        for root, directories, filenames in os.walk('src/cogs'):
            for filename in filenames:
                if filename.endswith(".py"):
                    directory = regsplit(r'[/\\]', root)[-1]
                    cogs_directory = directory == 'cogs'

                    # because we're in utils here we need to up a directory
                    # so to load the janitor cog from src/cogs/janitor/janitor.py, it needs to look like ..cogs.janitor.janitor
                    extension_prefix = "..cogs" if cogs_directory else f"..cogs.{directory}"
                    initial_extensions.append(f"{extension_prefix}.{filename[:-3]}")

        # Here we load our extensions(cogs) listed above in [initial_extensions].
        for extension in initial_extensions:
            self.bot.load_extension(name = extension, package = __package__)

        self.event_handlers.initialize()
        self.command_handlers.initialize()
        self.bot.run(os.getenv('BOT_KEY'))
