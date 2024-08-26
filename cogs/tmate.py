import datetime
import os
from typing import Optional
from discord.ext import commands
from loguru import logger
from discord.ext.commands.context import Context
from discord.ext.commands.bot import Bot
from discord import Embed, File
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

    def tmate_files(self):
        path = os.path.realpath(os.path.dirname(__file__)) + os.path.sep
        tmate_thumb = path + "files/tmate_thumb.jpeg"

        return {"tmate_thumb": tmate_thumb}

    def get_authorized_users(self):
        return ["saltycatfish", "het_tanis", "cre4t1v3"]

    def is_authorized(self, ctx: Context):
        return str(ctx.message.author).strip() in self.get_authorized_users()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__} is online")

    @commands.command()
    async def lab_link(self, ctx: Context):
        """Create a link with tmate for users to connect to a lab.

        Args:
            ctx (Context): Discord Context Class
        """
        logger.info(f"{self.uri}")
        msg = Embed(
            title="Lab Link URL",
            description="Click the link to jump to the lab",
            timestamp=datetime.datetime.now(),
            colour=discord.Colour.from_str("992d22"),
        )
        msg.add_field(name="TMate URI", value=f"https://{self.uri}")
        # Create a filename attachement for the thumbnail.
        image_thumbnail = File(
            f"{self.tmate_files()['tmate_thumb']}", filename="tmate_thumb.jpeg"
        )
        msg.set_thumbnail(url=f"attachment://{image_thumbnail.filename}")
        logger.debug(f"{msg.to_dict()}")
        logger.info("sending message")
        await ctx.send(embed=msg, file=image_thumbnail)
        await ctx.message.author.send(embed=msg, file=image_thumbnail)

    @commands.command()
    async def set_uri(self, ctx: Context, url: Optional[str] = None):
        logger.debug(f"set_uri: {ctx.message.author}")

        # Verify for a URL, also some regex as well.
        if url is None or url == "":
            await ctx.message.author.send("No URL provided.")
            return

        if self.is_authorized(ctx):
            uri = str(ctx.message.content[8:]).strip()
            with open("./uri", "w", encoding="utf-8") as _file:
                logger.debug(f"storing uri as {uri}")
                _file.write(uri)  # TODO must pass tmate uri validation

            await ctx.message.author.send(f"lab link changed to : {uri}")
        return


async def setup(bot):
    """
    Sets up the bot.
    """
    await bot.add_cog(TMate(bot))
