import os
from dotenv import load_dotenv

from src.utils.bot_factory import BotFactory


def main():
    load_dotenv()

    prefix = os.getenv('DISCORD_PREFIX')
    bot = BotFactory(prefix or "!")

    bot.start()


if __name__ == "__main__":
    main()
