import discord

from discord.ext import commands


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all(),
            help_command=None,
            description="Discord Interface for https://doomsday-clock-for-archie.vercel.app/",
        )

    async def setup_hook(self):
        await self.load_extension("src.commands")

    async def on_connect(self):
        print("Bot Connected!")

    async def on_disconnect(self):
        print("Bot is Disconnected!!")

    async def on_ready(self):
        await self.tree.sync()

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Watching over the cute siblinghood",
            ),
        )
