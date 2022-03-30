import discord


class EventHandler:

    def __init__(self, bot, cache):
        self.bot = bot
        self.cache = cache

    def initialize(self):
        @self.bot.event
        async def on_ready():
            print('Logged in as {0.user}'.format(self.bot))

        @self.bot.event
        async def on_message(message: discord.Message):
            if message.author == self.bot.user:
                return

            if message.channel.id in self.cache.keys():
                mirror_channel_id = self.cache[message.channel.id]
                await message.guild.get_channel(mirror_channel_id).send(message.content)

            await self.bot.process_commands(message)