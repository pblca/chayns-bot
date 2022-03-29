import os
import discord
from discord.ext import commands

from src.commands.command_handlers import CommandHandler
from src.events.event_handlers import EventHandler


class BotFactory:

    def __init__(self, prefix: str):
        intents = discord.Intents().all()
        self.bot = commands.Bot(command_prefix=prefix, intents=intents)
        self.event_handlers = EventHandler(self.bot)
        self.command_handlers = CommandHandler(self.bot)

    def start(self):
        self.event_handlers.initialize()
        self.command_handlers.initialize()
        self.bot.run(os.getenv('BOT_KEY'))
