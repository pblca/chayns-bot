from dotenv import load_dotenv

from src.utils.bot_factory import BotFactory

load_dotenv()

bot = BotFactory('!')
bot.start()
