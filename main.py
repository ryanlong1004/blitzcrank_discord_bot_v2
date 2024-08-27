import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger
from modals.request import RequestModal
from tasks.status import change_bot_status

# Load environment variables from the .env file, force overwriting.
load_dotenv(override=True)

# Constants
BOT_NAME = os.getenv("BOT_NAME", "GenericBot")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Ensure the Discord token is set
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not set.")

# Discord bot intents and configuration
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """
    This event is called when the bot is ready and connected to Discord.
    It also starts the bot's status update task and syncs the bot's slash commands.
    """
    change_bot_status.start(bot)  # Start the bot's status update task

    try:
        synced_commands = await bot.tree.sync()  # Sync the bot's slash commands
        logger.info(f"Successfully synced {len(synced_commands)} commands.")
    except Exception as e:
        logger.error("Failed to sync commands:", e)


@bot.tree.command()
async def request(interaction: discord.Interaction):
    """
    A slash command that triggers the request modal, allowing users to submit requests.

    :param interaction: The interaction object representing the command invocation.
    """
    await interaction.response.send_modal(RequestModal())


async def load_extensions():
    """
    Loads all cog extensions from the cogs directory.
    Each cog is a Python file that contains additional bot functionality.
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                logger.info(f"Loaded extension: {cog_name}")
            except Exception as e:
                logger.error(f"Failed to load extension {cog_name}: {e}")


@commands.Cog.listener()
async def on_message(self, message):
    logger.info(f"Incoming message: {message.content}")


async def main():
    """
    The main entry point for running the bot.
    It loads extensions and starts the bot with the provided token.
    """
    async with bot:
        await load_extensions()  # Load all extensions (cogs)
        await bot.start(str(DISCORD_TOKEN))  # Start the bot


if __name__ == "__main__":
    asyncio.run(main())
