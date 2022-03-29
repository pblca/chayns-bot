import discord


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

            await self.bot.process_commands(message)
