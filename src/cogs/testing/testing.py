import os

import discord
import sqlalchemy.orm
from discord.ext import commands
from discord import app_commands
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from db.models import Guild


load_dotenv()


class Testing(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.engine = self.bot.engine

    @app_commands.command(name='pull', description="example db pull from guilds")
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def pull(self, interaction: discord.Interaction):
        self.engine.connect()
        session: sqlalchemy.orm.Session = sessionmaker(bind=self.engine)()
        userdata = [guild.id for guild in session.query(Guild).all()]
        await interaction.response.send_message(f'db guild id info {userdata}')
        session.close()

    @app_commands.command(name='bing', description="fuck ya life")
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def bing(self, interaction: discord.Interaction):
        await interaction.response.send_message('bong')


async def setup(bot):
    await bot.add_cog(Testing(bot))
