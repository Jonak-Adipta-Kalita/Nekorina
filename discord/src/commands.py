import discord

from discord.ext import commands
from discord import app_commands
from src.bot import DiscordBot


class Commands(commands.Cog):
    def __init__(self, bot: DiscordBot):
        self.bot = bot

    @app_commands.command(name="update", description="Update the message")
    @app_commands.describe(
        time="Set the Time of the Clock",
        message="Set the Message",
        name="Authentication Name",
        password="Authentication Password",
    )
    async def update_message(
        self,
        inter: discord.Interaction,
        time: int,
        message: str,
        name: str,
        password: str,
    ):
        # await inter.response.send_message(f"{message} - {time} | Test Message")
        pass


async def setup(bot: DiscordBot):
    await bot.add_cog(Commands(bot))
