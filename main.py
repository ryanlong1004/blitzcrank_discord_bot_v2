import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger
from tasks.status import change_bot_status

# Load environment variables from .env file
load_dotenv()

# Constants
BOT_NAME = os.getenv("BOT_NAME")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Discord bot intents and configuration
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


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


@bot.event
async def on_ready():
    """
    Called when the bot is ready and has connected to Discord.
    """
    change_bot_status.start(bot)  # Start the bot's status update task

    # Sync the bot's slash commands
    try:
        synced_commands = await bot.tree.sync()
        logger.info(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        logger.error("Error syncing commands: ", e)


@bot.tree.command()
async def request(interaction: discord.Interaction):
    """
    Slash command to initiate the request modal.
    """
    await interaction.response.send_modal(RequestModal())


async def load_extensions():
    """
    Loads all cog extensions from the cogs directory.
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    """
    Main entry point for running the bot.
    """
    async with bot:
        await load_extensions()
        await bot.start(str(DISCORD_TOKEN))


if __name__ == "__main__":
    asyncio.run(main())
