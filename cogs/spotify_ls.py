import datetime
from loguru import logger
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.bot import Bot

# TODO Percentage Bar for times

class Spotify_ls(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__} is online")

    @commands.command(name='wltw')
    async def who_listening_to_spotify(self, ctx: Context, *users: discord.Member):
        """
        wltw = Who is Listening To What
        Lists users who are currently listening to Spotify and shows the remaining time of the song.
        If specific users are mentioned, it will only check those users.
        Usage:
        !wltw - Checks all users in the server.
        !wltw @user1 @user2 - Checks only the specified users.
        """
        users_listening = []

        # If no specific users are provided, check all server members
        members_to_check = users if users else ctx.guild.members

        # Iterate through the specified members (or all members if none specified)
        for member in members_to_check:
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):  # Check if the activity is Spotify
                    # Verify there is an artist for the track, podcast usually have this issue it seems.
                    artist = activity.artist if activity.artist else "Unknown Artist"

                    # Calculate the elapsed time
                    elapsed_time = datetime.datetime.now(datetime.UTC) - activity.start
                    remaining_time = activity.duration - elapsed_time

                    # Format the elapsed time and remaining time
                    elapsed_minutes, elapsed_seconds = divmod(int(elapsed_time.total_seconds()), 60)
                    elapsed_time_formatted = f"{elapsed_minutes}m {elapsed_seconds}s"

                    remaining_minutes, remaining_seconds = divmod(int(remaining_time.total_seconds()), 60)
                    remaining_time_formatted = f"{remaining_minutes}m {remaining_seconds}s"

                    # Format the message to send
                    song_info = (f"{member.display_name} is listening to '{activity.title}' by {artist}\nRemaining time: {remaining_time_formatted} Current time: {elapsed_time_formatted}")
                    users_listening.append(song_info) 

        # Prepare the response message
        response = "\n".join(users_listening) if users_listening else (
            "No specified users are currently listening to Spotify." if users else "No one is currently listening to Spotify.")
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Spotify_ls(bot))
