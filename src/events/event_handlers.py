import discord


class EventHandler:

    def __init__(self, bot):
        self.bot = bot

    def initialize(self):
        bot = self.bot

        @bot.event
        async def on_ready():
            print('Logged in as {0.user}'.format(bot))

        @bot.event
        async def on_message(message: discord.Message):
            if message.author == bot.user:
                return

            await bot.process_commands(message)