import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger
from modals.request import RequestModal
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
