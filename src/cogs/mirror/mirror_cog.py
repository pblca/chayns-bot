import datetime
import os
import time
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from sqlalchemy.orm import Session, sessionmaker

from data.cache import cache
from db.models import Channel
from src.utils.connectors import r

load_dotenv()


class Mirror(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        session: Session = sessionmaker(bind=self.bot.engine)()
        channels = filter(lambda _channel: _channel.mirror_to_channel_id is not None, session.query(Channel).all())
        #r.hmset('mirror_cache', {})
        cache['mirror_cache'] = {}
        count = 0
        for channel in channels:
            cache['mirror_cache'][channel.id] = channel.mirror_to_channel_id
            count += 1
        print(f'Mirror managing {count} channel(s)')
        session.close()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if 'mirror_cache' in cache and message.channel.id in cache['mirror_cache']:
            mirror_channel_id = cache['mirror_cache'][message.channel.id]
            embed = discord.Embed(color=0xFFFFFF)

            embed.set_footer(icon_url=message.author.avatar.url,
                             text=message.author.name)

            embed.add_field(name="[POST]", value=message.content)
            embed.timestamp = datetime.datetime.now()
            await message.guild.get_channel(mirror_channel_id).send(
                embed=embed,
                suppress_embeds=False
            )

    @app_commands.command(name='mirror')
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def mirror(self, interaction: discord.Interaction, channel: discord.TextChannel):
        session: Session = sessionmaker(bind=self.bot.engine)()
        db_channel = session.query(Channel).get(interaction.channel_id)
        mirror_channel = session.query(Channel).get(channel.id)

        if mirror_channel is None:
            mirror_channel = Channel(id=channel.id,
                                     guild_id=interaction.guild_id,
                                     mirror_to_channel_id=None)
            session.add(mirror_channel)
            session.commit()

        if db_channel is None:
            db_channel = Channel(id=interaction.channel_id,
                                 guild_id=interaction.guild_id,
                                 mirror_to_channel_id=channel.id)
            session.add(db_channel)
            session.commit()

        match cache:
            case {'mirror_cache': _}:
                cache['mirror_cache'][interaction.channel_id] = channel.id
                db_channel.mirror_to_channel_id = channel.id
                session.commit()
            case _:
                cache['mirror_cache']: dict = {interaction.channel_id, channel.id}
                db_channel.mirror_to_channel_id = channel.id
                session.commit()
        session.close()

        await interaction.response.send_message(f'Mirroring {interaction.channel_id} into {channel.mention}!')
        time.sleep(2)
        await interaction.delete_original_message()


async def setup(bot):
    await bot.add_cog(Mirror(bot))
