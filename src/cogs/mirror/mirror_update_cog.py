import datetime
import json

import discord
from discord import ChannelType
from discord.ext import commands
from discord import TextChannel
from discord import Thread

from src.utils.connectors import r
from src.utils.misc import str2int


class MirrorUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self):
    # r.hset('mirror_update_cache:')

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if (update_data := r.hgetall(f'mirror_update_cache:{before.id}')) \
                and before.author.id != self.bot.user.id:
            mirror_channel = await self.bot.fetch_channel(update_data['mirror_channel_id'])
            mirror_message = await mirror_channel.fetch_message(update_data['mirror_message_id'])
            embed = discord.Embed(color=0xFFFFFF)
            embed.set_footer(icon_url=after.author.avatar.url,
                             text=after.author.name)
            embed.add_field(name=f"[edit] from #{after.channel.name}", value=after.clean_content)
            embed.timestamp = datetime.datetime.now()
            if 'mirror_update_thread_id' in update_data and (thread_id := update_data['mirror_update_thread_id']):
                thread = mirror_channel.get_thread(int(thread_id))
                await thread.send(mirror_message.content)
            else:
                thread = await mirror_message.create_thread(name=f'_/--Update Log-==', reason='an edit was made to a '
                                                                                              'mirrored channel post')
                await thread.send(mirror_message.content)
                r.hset(f'mirror_update_cache:{before.id}', 'mirror_update_thread_id', thread.id)

            await mirror_message.edit(content=f'```\n{after.author.nick} from {after.channel.name} \n{after.clean_content}\n```')


async def setup(bot: commands.Bot):
    await bot.add_cog(MirrorUpdate(bot))
