import discord
import credentials

from typing import Optional
from discord.ext import commands
from discord import app_commands
from src.bot import DiscordBot


def authenticate(user: str) -> (bool, str, bool):
    view_allowed = False
    name = ""
    edit_allowed = False

    if user == credentials.BRO_ID:
        view_allowed = True
        name = credentials.BRO_NAME
        edit_allowed = True
    elif user == credentials.SIS_ID:
        view_allowed = True
        name = credentials.SIS_NAME
        edit_allowed = True
    elif user in credentials.SPECTATOR_IDS.split(","):
        view_allowed = True
        edit_allowed = False
    else:
        view_allowed = False
        edit_allowed = False

    return view_allowed, name, edit_allowed


class Commands(commands.Cog):
    def __init__(self, bot: DiscordBot):
        self.bot = bot

    @app_commands.command(name="update", description="Update the message")
    @app_commands.describe(
        time="Set the Time of the Clock",
        message="Set the Message",
    )
    @app_commands.choices(
        time=[app_commands.Choice(name=str(i), value=i) for i in range(1, 13)]
    )
    async def update_message(
        self,
        inter: discord.Interaction,
        time: int,
        message: str,
    ):
        view_allowed, name, edit_allowed = authenticate(str(inter.user.id))

        if not view_allowed:
            return await inter.response.send_message("Hey, Its None of your Business!")

    @app_commands.command(name="list", description="List the message(s)")
    @app_commands.describe(all="Whether to show the whole List, or only the Latest")
    async def get_messages(
        self, inter: discord.Interaction, all: Optional[bool] = None
    ):
        view_allowed, name, edit_allowed = authenticate(str(inter.user.id))

        if not view_allowed:
            return await inter.response.send_message("Hey, Its None of your Business!")


async def setup(bot: DiscordBot):
    await bot.add_cog(Commands(bot))
