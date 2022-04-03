import discord
import sqlalchemy
from discord.ext import commands
from discord.ext.commands import Context
from sqlalchemy.orm import sessionmaker

from data.cache import cache
from db.models import Guild
from src.events.message_analysis import message_analysis


class EventHandler:

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.engine: bot.engine

    def initialize(self):
        @self.bot.event
        async def on_ready(*args):
            print('Logged in as {0.user}'.format(self.bot))

            print('Registering New Guilds ...')
            # Open an orm session to compare db data with bot data
            session: sqlalchemy.orm.Session = sessionmaker(bind=self.bot.engine)()
            cache['guild_ids'] = [guild.id for guild in self.bot.guilds]
            db_guild_ids = [guild.id for guild in session.query(Guild).all()]
            guilds = [Guild(id=guild.id) for guild in filter(lambda guild: guild.id not in db_guild_ids, self.bot.guilds)]

            # Initial Command Import
            for guild in guilds:
                try:
                    info = await self.bot.tree.sync(guild=discord.Object(guild.id))
                    print(f'-- {guild.id}\n')
                    for inf in info:
                        print(f'----- Updated {inf.name}')

                except discord.HTTPException as ex:
                    print(ex)

            session.bulk_save_objects(guilds)
            session.commit()
            session.close()
            print(f'finished ( added {len(guilds)} ) ')

        @self.bot.event
        async def on_message(message: discord.Message):
            if message.author == self.bot.user:
                return

            message_analysis(message)
            await self.bot.process_commands(message)
