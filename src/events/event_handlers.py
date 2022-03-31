import discord

from src.events.message_analysis import message_analysis


class EventHandler:

    def __init__(self, bot):
        self.bot = bot

    def initialize(self):
        @self.bot.event
        async def on_ready():
            print('Logged in as {0.user}'.format(self.bot))

        @self.bot.event
        async def on_message(message: discord.Message):
            if message.author == self.bot.user:
                return

            message_analysis(message)

            await self.bot.process_commands(message)
