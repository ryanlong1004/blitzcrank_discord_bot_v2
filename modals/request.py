import discord
from loguru import logger


class RequestModal(discord.ui.Modal):
    """
    A modal for users to submit requests. Upon submission, the request is sent
    to a designated channel for moderators to review.
    """

    def __init__(self):
        """
        Initializes the RequestModal with a single text input field for the request.
        """
        super().__init__(title="Make a request")

        # Create a text input field for the request message
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
        Handles the submission of the request modal. Sends a confirmation message
        to the user and forwards the request to a moderator-only channel.

        :param interaction: The interaction object representing the user's interaction with the modal.
        """
        # Send a confirmation message to the user
        await interaction.response.send_message(
            "Thanks! We received your request.", ephemeral=True
        )

        # Ensure the interaction is within a guild context
        if interaction.guild is None:
            logger.warning("Interaction occurred outside of a guild context.")
            return

        # Find the channel named 'moderator-only' in the guild
        channel = discord.utils.get(interaction.guild.channels, name="moderator-only")
        if channel is None or isinstance(
            channel, (discord.ForumChannel, discord.CategoryChannel)
        ):
            logger.error("Channel 'moderator-only' not found or is of an invalid type.")
            return

        # Send the user's request to the moderator-only channel test
        await channel.send(f"User Requesterssssss: \n\n{self.request.value}")
