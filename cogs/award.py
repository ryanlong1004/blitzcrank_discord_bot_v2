import datetime
import os
from typing import Optional
from discord.ext import commands
from loguru import logger
from discord.ext.commands.context import Context
from discord.ext.commands.bot import Bot
from discord import Embed, Member, File


class Award(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    def get_authorized_users(self):
        # List of users by id that are authorized to run the command.
        # 142508669999775754 = 創意
        # 611026501671976975 = het_tanis
        return ["142508669999775754", "611026501671976975"]

    def is_authorized(self, ctx: Context):
        return str(ctx.message.author.id) in self.get_authorized_users()

    def award_files(self):
        path = os.path.realpath(os.path.dirname(__file__)) + os.path.sep
        award = path + "files/360_F_446459957_nIy330lOKvQ5N92WpIn5zPElIikTRB4g-1551506731.jpg"
        self_award = path + "files/XJGc.jpg"

        return {"award": award, "self_award": self_award}

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__} is online")

    @commands.command()
    async def award(
        self,
        ctx: Context,
        member: Optional[Member] = None,
        *,
        description: Optional[str] = None,
    ):
        """Generate the command to be sent.

        Args:
            ctx (Context): Discord Context Class
            member (Optional[Member], optional): Discord Member Class. Defaults to None.
            description (Optional[str], optional): Description for the award. Defaults to None.
        """
        # Verify the user is authorized to run the command
        if not self.is_authorized(ctx):
            await ctx.send("You are simply not cool enough to award someone.. yet.")
            return

        # Check if a valid member was provided.
        if member is None:
            await ctx.send("Are you giving the award to the air or a user?")
            logger.info(f"Incorrect user?: {member}")
            return

        if description is None:
            description = "You've earned an awesome award!"

        # Do not let users award themselves.
        if ctx.message.author.id == member.id:
            msg = Embed(
                title="Hahaha, trying to award yourself?!",
                color=0x6F4F28,  # https://old.discordjs.dev/#/docs/discord.js/main/typedef/Colors
                timestamp=datetime.datetime.now(),
            )
            image = File(f'{self.award_files()["self_award"]}', filename="self_award.png")
            msg.set_image(url=f"attachment://{image.filename}")  # Ai maybe?
            logger.debug(f"Embed Message: {msg.to_dict()}")
            logger.info(f"Sending reward to {member.display_name}...")
            await ctx.send(embed=msg, file=image)
            return

        # Message to send awarded user
        await ctx.send(f"### 🎉{member.mention} has been given an award! 🎉".upper())
        msg = Embed(
            title=f"The Kings To you Award:\n{member.display_name.upper()}",
            description=description + " 🏆\n",
            color=0xFFD700,  # Gold color in hexadecimal
            timestamp=datetime.datetime.now(),
        )
        # msg.set_thumbnail(url="http://0x0.st/XysE.png")
        image = File(f'{self.award_files()["award"]}', filename="award.png")
        msg.set_image(url=f"attachment://{image.filename}")  # Ai maybe?
        logger.debug(f"Embed Message: {msg.to_dict()}")
        logger.info(f"Sending award to {member.display_name}...")
        await ctx.send(embed=msg, file=image)


async def setup(bot):
    await bot.add_cog(Award(bot))
