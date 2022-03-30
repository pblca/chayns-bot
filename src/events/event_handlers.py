import discord


class EventHandler:

    def __init__(self, bot, cache):
        self.bot = bot
        self.cache: dict = cache

    def initialize(self):
        @self.bot.event
        async def on_ready():
            print('Logged in as {0.user}'.format(self.bot))

        @self.bot.event
        async def on_message(message: discord.Message):
            if message.author == self.bot.user:
                return

            if 'mirror_cache' in self.cache.keys() and message.channel.id in self.cache['mirror_cache'].keys():
                mirror_channel_id = self.cache['mirror_cache'][message.channel.id]
                await message.guild.get_channel(mirror_channel_id).send(
                    f"[{message.created_at}] [{message.channel.name}] \n[{message.author.name}] : {message.content}")

            await self.bot.process_commands(message)