import discord.ui
from discord import ButtonStyle


class DeleteView(discord.ui.View):
    @discord.ui.button(label='Remove', style=ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button):
        await interaction.message.delete()
