# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import asyncio
import os
import discord
from discord.ext import commands

from dotenv import load_dotenv


from loguru import logger

from tasks.status import change_bot_status

load_dotenv()

BOT_NAME = "Blitzcrank"


intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def get_guild_count():
    # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
    guild_count = 0

    # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in bot.guilds:
        # PRINT THE SERVER'S ID AND NAME.
        logger.info(f"- {guild.id} (name: {guild.name})")

        # INCREMENTS THE GUILD COUNTER.
        guild_count = guild_count + 1

    logger.info(f"{guild_count} total guilds")


@bot.event
async def on_ready():

    # load tasks
    change_bot_status.start(bot)

    # meh ....

    try:
        synced_commands = await bot.tree.sync()
        logger.info(f"Synced {len(synced_commands)}")
    except Exception as e:
        logger.error("errors syncing commands", e)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    print(os.environ["DISCORD_TOKEN"])
    async with bot:
        await load()
        await bot.start(os.environ["DISCORD_TOKEN"])


asyncio.run(main())
