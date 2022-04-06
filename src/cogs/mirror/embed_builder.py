import datetime
from collections.abc import Sequence
import textwrap
from functools import partial
from io import StringIO

import discord


def get_embeds_from_string(content, message: discord.Message, edit: bool, delete: bool = False) -> Sequence[discord.Embed]:
    embeds = []
    embed_contents = [l for l in iter(partial(StringIO(content).read, 900), '')]
    head_tail_iter = iter(embed_contents)
    emb = discord.Embed(color=0xFFFFFF if not edit else 0xE2DC22,
                        timestamp=datetime.datetime.now())
    emb.set_footer(text=message.author.nick or message.author.name,
                   icon_url=message.author.guild_avatar or message.author.avatar)
    first_content = next(head_tail_iter)
    icon = '❓'
    match edit, delete:
        case _, True:
            icon = '❌'
        case True, False:
            icon = '✏️'
        case False, False:
            icon = '💬'

    emb.add_field(
        name=f'{icon} {message.author.nick or message.author.name} from #{message.channel.name}',
        value=first_content)
    embeds.append(emb)
    if len(first_content) > 300:
        emb.set_thumbnail(url=message.author.guild_avatar or message.author.avatar)

    for c in head_tail_iter:
        embed = discord.Embed(color=0xFFFFFF)
        embed.add_field(name=f'(contd)', value=c)
        embeds.append(embed)

    return embeds
