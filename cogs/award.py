from typing import Optional
from discord.ext import commands
from loguru import logger
from discord.ext.commands.context import Context
from discord.ext.commands.bot import Bot
from discord import Embed, Member

class Award(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    def get_authorized_users(self):
        # List of users that are authorized to run the command.\
        # 142508669999775754 = 創意
        # 611026501671976975 = het_tanis
        return ["142508669999775754", "611026501671976975"]

    def is_authorized(self, ctx: Context):
        return str(ctx.message.author.id) in self.get_authorized_users()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__} is online")

    @commands.command()
    async def reward(self, ctx: Context, member: Optional[Member] = None):
        # Verify the user is authorized to run the command
        if not self.is_authorized(ctx):
            await ctx.send("You are simply not cool enough to award someone.. yet.")
            return

        # Check if a valid member was provided.
        if member is None:
            await ctx.send("Are you giving the award to the air or a user?")
            logger.info(f"Incorrect user?: {member}")
            return

        # Do not let users award themselves.
        if ctx.message.author.id == member.id:
            msg = Embed(
            title="Hahaha, trying to award yourself?!",
            color=0x6F4F28 # https://old.discordjs.dev/#/docs/discord.js/main/typedef/Colors
            )
            msg.set_image(url="http://0x0.st/XJGc.jpg")  # Ai maybe?
            logger.debug(f"Embed Message: {msg.to_dict()}")
            logger.info(f"Sending reward to {member.display_name}...")
            await ctx.send(embed=msg)
            return

        msg = Embed(
            title="Achievement Unlocked! 🥳",
            description=f"**Congratulations {member.mention}!**\n\nYou've earned an awesome award! 🏆\n",
            color=0xFFD700  # Gold color
        )
        msg.set_thumbnail(url="https://i.imgur.com/0gNJUsh.png")
        msg.set_image(url="http://0x0.st/XJ05.gif")  # Ai maybe?

        logger.debug(f"Embed Message: {msg.to_dict()}")
        logger.info(f"Sending award to {member.display_name}...")
        await ctx.send(embed=msg)
        await ctx.send(f"{member.mention}, 🎉 you have been awarded! 🏆")


async def setup(bot):
    await bot.add_cog(Award(bot))