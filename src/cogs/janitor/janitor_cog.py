import os
import time

import discord
import sqlalchemy.orm
from discord.ext import commands
from discord import app_commands, Interaction

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from data.cache import cache
from db.models import Channel

load_dotenv()


class Janitor(commands.Cog):

    def __init__(self, _bot: discord.ext.commands.Bot):
        self.bot: commands.Bot = _bot

    @commands.Cog.listener()
    async def on_ready(self):
        session: sqlalchemy.orm.Session = sessionmaker(bind=self.bot.engine)()
        channels = filter(lambda _channel: _channel.janitor_limit is not None, session.query(Channel).all())
        cache['janitor_cache'] = {}
        count = 0
        for channel in channels:
            cache['janitor_cache'][channel.id] = \
                {'limit': channel.janitor_limit, 'frequency': channel.janitor_frequency, 'message_count': [0]}
            count += 1
        print(f'Janitor managing {count} channel(s)')
        session.close()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        match cache:
            case {'janitor_cache': {message.channel.id: current_cache}}:
                count = current_cache['message_count']
                count[0] += 1
                if count[0] >= current_cache['limit']:
                    count[0] -= current_cache['frequency']
                    await message.channel.purge(limit=current_cache['frequency'], check=lambda x: True)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        match cache:
            case {'janitor_cache': {message.channel.id: current_cache}}:
                current_cache['message_count'][0] -= 1

    @app_commands.command(name="janitor", description="Enforces a set limit of message after command execution")
    @app_commands.guilds(int(int(os.getenv('TEST_GUILD'))))
    async def janitor(self, interaction: Interaction, limit: int = 200, frequency: int = 5):
        janitor_information = {'limit': limit, 'frequency': frequency, 'message_count': [0]}
        session: sqlalchemy.orm.Session = sessionmaker(bind=self.bot.engine)()
        channel = session.query(Channel).get(interaction.channel_id)
        if channel is None:
            channel = Channel(id=interaction.channel_id,
                              guild_id=interaction.guild_id,
                              janitor_limit=limit,
                              janitor_frequency=frequency)
            session.add(channel)
            session.commit()

        match cache:
            case {"janitor_cache": _}:
                cache['janitor_cache'][interaction.channel_id] = janitor_information
            case _:
                cache['janitor_cache']: dict = {interaction.channel_id: janitor_information}
                channel.janitor_limit = limit
                channel.janitor_frequency = frequency
                session.commit()

        session.close()

        await interaction.response.send_message("Janitor active.")
        time.sleep(2)
        await interaction.delete_original_message()


async def setup(_bot: commands.Bot):
    await _bot.add_cog(Janitor(_bot))
