import discord
import credentials

from typing import Optional
from discord.ext import commands
from discord import app_commands
from src.bot import DiscordBot
from src.embeds import embed_message, embed_all_messages, get_message_user
from datetime import datetime, timezone


def authenticate(inter: discord.Interaction) -> (bool, str, bool):
    user = str(inter.user.id)

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


class DoomsDayClock(app_commands.Group, name="clock", description="Commands for the Dooms Day Clock"):
    def __init__(self, bot: DiscordBot):
        super().__init__()

        self.bot = bot

        self.messages_ref = self.bot.messages_ref
        self.latest_message_ref = self.bot.latest_message_ref

    @app_commands.command(name="update", description="Update the message")
    @app_commands.describe(
        time="Set the Time of the Clock",
        message="Set the Message",
        hidden="Whether to have the messages Visible only to you!",
    )
    @app_commands.choices(
        time=[app_commands.Choice(name=str(i), value=i) for i in range(1, 13)]
    )
    async def update_message(
        self, inter: discord.Interaction, time: int, message: str, hidden: bool = False
    ):
        view_allowed, name, edit_allowed = authenticate(inter)

        if not view_allowed or not edit_allowed:
            return await inter.response.send_message(
                "Hey, Its None of your Business!", ephemeral=hidden
            )

        now = datetime.now(timezone.utc)
        timestamp = (
            now.strftime("%Y-%m-%dT%H:%M:%S.") +
            f"{now.microsecond // 1000:03d}Z"
        )

        username = ""
        if str(inter.user.id) == credentials.BRO_ID:
            username = credentials.BRO_NAME
        elif str(inter.user.id) == credentials.SIS_ID:
            username = credentials.SIS_NAME

        message_obj = {
            "message": message,
            "time": time,
            "timestamp": timestamp,
            "user": username,
        }

        latest_message = self.latest_message_ref.get().to_dict()
        self.messages_ref.document(
            latest_message["timestamp"]).set(latest_message)
        self.latest_message_ref.set(message_obj)

        embed = embed_message(message_obj, inter.user)

        return await inter.response.send_message(
            "Updated Clock!", embed=embed, ephemeral=hidden
        )

    @app_commands.command(name="list", description="List the message(s)")
    @app_commands.describe(
        all="Whether to show the whole List, or only the Latest",
        hidden="Whether to have the messages Visible only to you!",
    )
    async def get_messages(
        self,
        inter: discord.Interaction,
        all: Optional[bool] = None,
        hidden: bool = False,
    ):
        view_allowed, name, edit_allowed = authenticate(inter)

        if not view_allowed:
            return await inter.response.send_message(
                "Hey, Its None of your Business!", ephemeral=hidden
            )

        if bool(all):
            snapshot = self.messages_ref.stream()
            messages = [{"id": doc.id, **doc.to_dict()} for doc in snapshot]
            embed, view = await embed_all_messages(messages, self.bot)

            return await inter.response.send_message(
                embed=embed, view=view, ephemeral=hidden
            )
        else:
            latest_message = self.latest_message_ref.get()

            if latest_message.exists:
                msg = latest_message.to_dict()
                user = await get_message_user(msg["user"], self.bot.fetch_user)
                embed = embed_message(msg, user)

                return await inter.response.send_message(embed=embed, ephemeral=hidden)
            else:
                return await inter.response.send_message(
                    "There are no messages, go to the website!", ephemeral=hidden
                )


class Commands(commands.Cog):
    def __init__(self, bot: DiscordBot):
        self.bot = bot
        self.bot.tree.add_command(DoomsDayClock(bot))


async def setup(bot: DiscordBot):
    await bot.add_cog(Commands(bot))
