# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import asyncio
import os
import discord
from discord.ext import commands

from dotenv import load_dotenv


from loguru import logger

from tasks.status import change_bot_status

load_dotenv()

BOT_NAME = os.environ["BOT_NAME"]


class RequestModal(discord.ui.Modal, title="Make a request"):
    request = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Message",
        required=True,
        max_length=500,
        placeholder="I'd like to learn more about ...",
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Thanks!  We received your request", ephemeral=True
        )
        assert interaction.guild is not None
        channel = discord.utils.get(interaction.guild.channels, name="moderator-only")
        assert channel.__class__.__name__ not in [
            None,
            discord.ForumChannel,
            discord.CategoryChannel,
        ]
        await channel.send(f"User Request: \n\n{self.request.value}")


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    change_bot_status.start(bot)
    try:
        synced_commands = await bot.tree.sync()
        logger.info(f"Synced {len(synced_commands)}")
    except Exception as e:
        logger.error("errors syncing commands", e)


@bot.tree.command()
async def request(interaction: discord.Interaction):
    await interaction.response.send_modal(RequestModal())


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(os.environ["DISCORD_TOKEN"])


asyncio.run(main())
