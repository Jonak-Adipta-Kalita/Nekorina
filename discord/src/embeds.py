import discord
import credentials

from datetime import datetime
from discord import Embed, Color, User
from discord.ui import View, Button
from discord.ext import commands


async def get_message_user(user: str, fetch) -> discord.User:
    user_id = None
    if user == credentials.BRO_NAME:
        user_id = credentials.BRO_ID
    elif user == credentials.SIS_NAME:
        user_id = credentials.SIS_ID

    return await fetch(user_id)


class PaginationView(View):
    def __init__(self, messages: list, bot: commands.Bot):
        super().__init__(timeout=60)

        self.messages = messages[::-1]
        self.bot = bot
        self.page = 0

    async def build_embed(self) -> discord.Embed:
        msg = self.messages[self.page]
        user = await get_message_user(msg["user"], self.bot.fetch_user)

        embed = discord.Embed(
            color=discord.Color.blue(),
            timestamp=datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00")),
        )
        embed.add_field(name="Message", value=msg["message"], inline=False)
        embed.add_field(name="Time of Clock", value=f"{
                        msg['time']}/12", inline=True)
        embed.set_footer(
            text=f"{user.name}  •  {self.page + 1}/{len(self.messages)}",
            icon_url=user.display_avatar.url,
        )

        return embed

    def update_buttons(self):
        self.prev.disabled = self.page == 0
        self.next.disabled = self.page == len(self.messages) - 1

    @discord.ui.button(label="◀", style=discord.ButtonStyle.secondary)
    async def prev(self, inter: discord.Interaction, button: Button):
        self.page -= 1
        self.update_buttons()
        await inter.response.edit_message(embed=await self.build_embed(), view=self)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.secondary)
    async def next(self, inter: discord.Interaction, button: Button):
        self.page += 1
        self.update_buttons()
        await inter.response.edit_message(embed=await self.build_embed(), view=self)


async def embed_all_messages(messages: list, bot: commands.Bot):
    view = PaginationView(messages, bot)
    view.update_buttons()
    return await view.build_embed(), view


def embed_message(message, user: User):
    embed = Embed(
        color=Color.blue(),
        timestamp=datetime.fromisoformat(message["timestamp"].replace("Z", "+00:00")),
    )

    embed.add_field(name="Message", value=message["message"], inline=False)
    embed.add_field(name="Time of Clock", value=f"{
                    message["time"]}/12", inline=True)

    embed.set_footer(text=user.name, icon_url=user.display_avatar.url)

    return embed
