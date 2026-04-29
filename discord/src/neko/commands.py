from nekosbest import Client as Neko

from discord.ext import commands
from discord import app_commands
from src.bot import DiscordBot
from src.neko.act_commands import add_act_commands
from src.neko.interactable_commands import InteractableCommands


class NekotinaCog(commands.Cog):
    def __init__(self, bot: DiscordBot, neko: Neko):
        self.bot = bot
        self.neko = neko

        self.nekotina = app_commands.Group(name="nekotina", description="Act uWu")

        add_act_commands(self.nekotina, self.bot, self.neko)
        self.nekotina.add_command(InteractableCommands(bot, neko))

        self.bot.tree.add_command(self.nekotina)


async def setup(bot: DiscordBot):
    await bot.add_cog(NekotinaCog(bot, Neko()))
