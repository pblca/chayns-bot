import os
import discord
from discord.ext import commands


from src.cogs.mirror.mirror import Mirror
from src.cogs.janitor.janitor import Janitor
from src.commands.command_handlers import CommandHandler
from src.events.event_handlers import EventHandler


class BotFactory:

    def __init__(self, prefix: str):
        intents = discord.Intents().all()
        self.cache: dict = {}
        self.bot = commands.Bot(command_prefix=prefix, intents=intents)
        self.event_handlers = EventHandler(self.bot, self.cache)
        self.command_handlers = CommandHandler(self.bot, self.cache)

    def start(self):
        self.event_handlers.initialize()
        self.command_handlers.initialize()
        self.bot.add_cog(Mirror(self.bot, self.cache))
        self.bot.add_cog(Janitor(self.bot, self.cache))
        self.bot.run(os.getenv('BOT_KEY'))
