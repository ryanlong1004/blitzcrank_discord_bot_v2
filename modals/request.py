import discord
from loguru import logger


class RequestModal(discord.ui.Modal):
    """
    A modal for users to submit requests. This will send a message to a designated channel
    for moderators to review.
    """

    def __init__(self):
        super().__init__(title="Make a request")

        # Request input field
        self.request = discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Message",
            required=True,
            max_length=500,
            placeholder="I'd like to learn more about ...",
        )
        self.add_item(self.request)

    async def on_submit(self, interaction: discord.Interaction):
        """
        Handles submission of the request modal.
        """
        await interaction.response.send_message(
            "Thanks! We received your request.", ephemeral=True
        )

        # Ensure the interaction has a guild context
        if interaction.guild is None:
            logger.warning("Interaction occurred outside of a guild context.")
            return

        # Find the designated channel for moderator review
        channel = discord.utils.get(interaction.guild.channels, name="moderator-only")
        if (
            isinstance(channel, (discord.ForumChannel, discord.CategoryChannel))
            or channel is None
        ):
            logger.error("Channel 'moderator-only' not found or is of an invalid type.")
            return

        # Send the user's request to the moderator-only channel
        await channel.send(f"User Request: \n\n{self.request.value}")
