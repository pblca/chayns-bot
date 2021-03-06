import os
import time

import discord
from discord.ext import commands
from discord import app_commands

from dotenv import load_dotenv

from data.cache import cache

load_dotenv()


class Watch(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if 'watch_cache' in cache and message.author.id in cache['watch_cache']:
            destination_channel_id = cache['watch_cache'][message.author.id]
            images = message.attachments
            colour = message.author.colour
            await message.guild.get_channel(destination_channel_id).send(embeds=[discord.Embed(
                description=message.content,
                colour=colour,
            ).set_author(name=f"{message.author.name}#{message.author.discriminator}",
                         icon_url=message.author.avatar.url)
                .set_image(
                    url=images.pop(0).url if len(images) > 0 else None)
                ,*[discord.Embed(
                    colour=colour).set_image(
                    url=img.url) for img in images]
            ])

    @app_commands.command(name="watch")
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def watch(self, interaction: discord.Interaction, user: discord.User, channel: discord.TextChannel):
        if 'watch_cache' not in cache:
            cache['watch_cache']: dict = {user.id: channel.id}
        else:
            cache['watch_cache'][user.id] = channel.id

        await interaction.response.send_message(embed=discord.Embed(
            colour=0x0FB964,
            description=f'**{user.name}** is now on the watchlist, they are being watched in {channel.mention}.'
        ))
        time.sleep(3)
        await interaction.delete_original_message()

    @app_commands.command(name="unwatch")
    @app_commands.guilds(int(os.getenv('TEST_GUILD')))
    async def unwatch(self, interaction: discord.Interaction, user: discord.User):
        if 'watch_cache' in cache and user.id in cache['watch_cache']:
            cache['watch_cache'].pop(user.id)
            await interaction.response.send_message(embed=discord.Embed(
                colour=0x0C74CC,
                description=f'**{user.name}** is no longer on the watchlist.'
            ))
            time.sleep(2)
            await interaction.delete_original_message()
        else:
            await interaction.response.send_message(embed=discord.Embed(
                colour=0x0C74CC,
                description=f'{user.name} was not on the watchlist.'
            ))
            time.sleep(2)
            await interaction.delete_original_message()


async def setup(bot):
    await bot.add_cog(Watch(bot))
