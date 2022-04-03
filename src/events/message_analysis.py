import discord

from data.bad_list import actionable_words


def message_analysis(message: discord.Message):
    if len([each for each in actionable_words if each.lower() in message.content.lower()]) > 0:
        print(f"{message.author.name} said a no no word")
