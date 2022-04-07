import os
import time

import discord
import sqlalchemy.orm
from discord.ext import commands
from discord import app_commands, Interaction, Thread

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from data.cache import cache
from db.models import Channel
from src.utils.connectors import r

load_dotenv()


class Janitor(commands.Cog):

    def __init__(self, _bot: discord.ext.commands.Bot):
        self.bot: commands.Bot = _bot

    @commands.Cog.listener()
    async def on_ready(self):
        session: sqlalchemy.orm.Session = sessionmaker(bind=self.bot.engine)()
        channels = filter(lambda _channel: _channel.janitor_limit is not None, session.query(Channel).all())
        count = 0
        for channel in channels:
            try:
                discord_channel = await self.bot.fetch_channel(channel.id)
                for thread in discord_channel.threads:
                    r.hset(f'janitor_cache:{channel.id}', f'message_count:{thread.id}', 0)
                    # I AM SO SORRY THIS IS LITERALLY THE ONLY WAY
                    try:
                        await thread.purge(limit=None, check=lambda m: not m.is_system())
                    except discord.errors.Forbidden:
                        print('life is pain')
            except discord.errors.NotFound as exception:
                print('channel deleted while offline')
                session.delete(channel)
                session.commit()
            r.hset(f'janitor_cache:{channel.id}', 'limit', channel.janitor_limit)
            r.hset(f'janitor_cache:{channel.id}', 'frequency', channel.janitor_frequency)
            r.hset(f'janitor_cache:{channel.id}', 'message_count', 0)
            count += 1
        print(f'Janitor managing {count} channel(s)')
        session.close()

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if current_cache := r.hgetall(f'janitor_cache:{thread.parent_id}'):
            r.hset(f'janitor_cache:{thread.parent_id}', f'message_count:{thread.id}', 0)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if type(message.channel) == discord.Thread:
            thread = message.channel
            if current_cache := r.hgetall(f'janitor_cache:{message.channel.parent_id}'):
                count = int(current_cache[f'message_count:{thread.id}'])
                r.hset(f'janitor_cache:{thread.parent_id}', f'message_count:{thread.id}', count+1)
                if count+1 > int(current_cache['limit']):
                    count -= int(current_cache['frequency'])
                    r.hset(f'janitor_cache:{thread.parent_id}', f'message_count:{thread.id}', count)
                    await message.channel.purge(limit=int(current_cache['frequency']),
                                                check=lambda x: True,
                                                oldest_first=True)
        else:
            if current_cache := r.hgetall(f'janitor_cache:{message.channel.id}'):
                count = int(current_cache['message_count'])
                r.hset(f'janitor_cache:{message.channel.id}', 'message_count', count+1)
                if count+1 >= int(current_cache['limit']):
                    count -= int(current_cache['frequency'])
                    r.hset(f'janitor_cache:{message.channel.id}', 'message_count',  count-int(current_cache['frequency']))
                    await message.channel.purge(limit=int(current_cache['frequency']),
                                                check=lambda x: True,
                                                oldest_first=True)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        match cache:
            case {'janitor_cache': {message.channel.id: current_cache}}:
                current_cache['message_count'][0] -= 1

    @app_commands.command(name="janitor", description="Enforces a set limit of message after command execution")
    @app_commands.guilds(int(int(os.getenv('TEST_GUILD'))))
    async def janitor(self, interaction: Interaction, limit: int = 200, frequency: int = 5):
        session: sqlalchemy.orm.Session = sessionmaker(bind=self.bot.engine)()
        channel = session.query(Channel).get(interaction.channel_id)
        if channel is None:
            channel = Channel(id=interaction.channel_id,
                              guild_id=interaction.guild_id,
                              janitor_limit=limit,
                              janitor_frequency=frequency)
            session.add(channel)
            session.commit()

        r.hset(f'janitor_cache:{interaction.channel_id}', 'limit', limit)
        r.hset(f'janitor_cache:{interaction.channel_id}', 'frequency', frequency)
        r.hset(f'janitor_cache:{interaction.channel_id}', 'message_count', 0)
        discord_channel = await self.bot.fetch_channel(interaction.channel_id)
        for thread in discord_channel.threads:
            r.hset(f'janitor_cache:{interaction.channel_id}', f'message_count:{thread.id}', 0)

        channel.janitor_limit = limit
        channel.janitor_frequency = frequency
        session.commit()
        session.close()

        await interaction.response.send_message("Janitor active.")
        time.sleep(2)
        await interaction.delete_original_message()


async def setup(_bot: commands.Bot):
    await _bot.add_cog(Janitor(_bot))
