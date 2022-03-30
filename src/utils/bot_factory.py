import os
import discord
from discord.ext import commands

from src.events.event_handlers import EventHandler


class BotFactory:

    def __init__(self, prefix: str):
        intents = discord.Intents().all()
        self.bot = commands.Bot(command_prefix=prefix, intents=intents)
        self.event_handlers = EventHandler(self.bot)

    def start(self):
        initial_extensions = ['..cogs.mod']
        # Here we load our extensions(cogs) listed above in [initial_extensions].
        #import pdb; pdb.set_trace()
        for extension in initial_extensions:
            self.bot.load_extension(name = extension, package = __package__)
        self.event_handlers.initialize()
        self.bot.run(os.getenv('BOT_KEY'))
