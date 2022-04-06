import datetime
import json

import discord
from discord import ChannelType
from discord.ext import commands
from discord import TextChannel
from discord import Thread

from src.cogs.mirror.embed_builder import get_embeds_from_string
from src.utils.connectors import r
from src.utils.misc import str2int


class MirrorUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, deleted_message: discord.Message):
        if (delete_data := r.hgetall(f'mirror_update_cache:{deleted_message.id}')) \
                and deleted_message.author.id != self.bot.user.id:
            mirror_channel = await self.bot.fetch_channel(delete_data['mirror_channel_id'])
            mirror_message = await mirror_channel.fetch_message(delete_data['mirror_message_id'])
            if 'mirror_update_thread_id' in delete_data and (thread_id := delete_data['mirror_update_thread_id']):
                thread = mirror_channel.get_thread(int(thread_id))
                await thread.send(embeds=mirror_message.embeds)
            else:
                thread = await mirror_message.create_thread(name=f'Message Edit Log', reason='an edit was made to a '
                                                                                             'mirrored channel post')
                await thread.send(embeds=mirror_message.embeds)
                r.hset(f'mirror_update_cache:{mirror_message.id}', 'mirror_update_thread_id', thread.id)

            await mirror_message.edit(
                embeds=get_embeds_from_string("(deleted)", deleted_message, True, True))

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if (update_data := r.hgetall(f'mirror_update_cache:{before.id}')) \
                and before.author.id != self.bot.user.id:
            mirror_channel = await self.bot.fetch_channel(update_data['mirror_channel_id'])
            mirror_message = await mirror_channel.fetch_message(update_data['mirror_message_id'])
            if 'mirror_update_thread_id' in update_data and (thread_id := update_data['mirror_update_thread_id']):
                thread = mirror_channel.get_thread(int(thread_id))
                await thread.send(embeds=mirror_message.embeds)
            else:
                thread = await mirror_message.create_thread(name=f'Message Edit Log', reason='an edit was made to a '
                                                                                              'mirrored channel post')
                await thread.send(embeds=mirror_message.embeds)
                r.hset(f'mirror_update_cache:{before.id}', 'mirror_update_thread_id', thread.id)

            await mirror_message.edit(
                embeds=get_embeds_from_string(after.clean_content, after, True))


async def setup(bot: commands.Bot):
    await bot.add_cog(MirrorUpdate(bot))
