import datetime
import os
from typing import Any
from discord.ext import commands
from loguru import logger
from discord.ext.commands.context import Context
from discord.ext.commands.bot import Bot
from discord import Embed
import discord


class TMate(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @property
    def uri(self):
        result = ""
        with open("./uri", "r", encoding="utf-8") as _file:
            result = _file.read()
        return result

    def get_authorized_users(self):
        return ["saltycatfish", "het_tanis"]

    def is_authorized(self, ctx: Context):
        return str(ctx.message.author).strip() in self.get_authorized_users()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__} is online")

    @commands.command()
    async def lab_link(self, ctx: Context):
        logger.info(f"{self.uri}")
        msg = Embed(
            title="Lab Link URL",
            description=f"Click the link to jump to the lab",
            color=discord.color.parse_hex_number("992d22"),
            timestamp=datetime.datetime.now(),
        )
        msg.add_field(name="TMate URI", value=f"https://{self.uri}")
        msg.set_thumbnail(url=os.environ["TMATE_THUMB_URL"])
        logger.debug(f"{msg.to_dict()}")
        logger.info("sending message")
        await ctx.message.author.send(embed=msg)

    @commands.command()
    async def set_uri(self, ctx: Context):
        logger.debug(f"set_uri: {ctx.message.author}")
        if self.is_authorized(ctx):
            uri = str(ctx.message.content[8:]).strip()
            with open("./uri", "w", encoding="utf-8") as _file:
                logger.debug(f"storing uri as {uri}")
                _file.write(uri)  # TODO must pass tmate uri validation

            await ctx.message.author.send(f"lab link changed to : {uri}")
        return


async def setup(bot):
    await bot.add_cog(TMate(bot))
