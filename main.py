import os
from dotenv import load_dotenv

from src.utils.bot_factory import BotFactory

load_dotenv()

prefix = os.getenv('DISCORD_PREFIX')
bot = BotFactory(prefix if prefix is None else "!")
bot.start()
