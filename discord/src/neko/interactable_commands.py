import discord
import random

from nekosbest import Client as Neko

from discord import app_commands
from src.neko.embeds import InteractableView, act_embed, buttons
from src.bot import DiscordBot
from src.neko.act_commands import get_act, is_interactable

from dataclasses import dataclass


@dataclass
class ButtonCfg:
    name: str
    emoji: str
    style: discord.ButtonStyle = discord.ButtonStyle.grey


punish_buttons = [
    ButtonCfg("Kick", "🦵"),
    ButtonCfg("Punch", "👊"),
    ButtonCfg("Shoot", "🔫"),
    ButtonCfg("Slap", "🖐️"),
]


class InteractableCommands(
    app_commands.Group, name="interact", description="uWu Interactable Commands"
):
    def __init__(self, bot: DiscordBot, neko: Neko, **kwargs):
        super().__init__(**kwargs)

        self.bot = bot
        self.neko = neko

    async def interact_command(
        self,
        inter: discord.Interaction,
        act_name: str,
        user: discord.User,
        buttons_cfg: list[dict],
    ):
        if inter.user.id == user.id:
            return await inter.response.send_message(
                "❌ Can't do that to yourself...", ephemeral=True
            )

        await inter.response.defer()
        data = await self.neko.get_image(act_name)

        act_data = get_act(act_name, True)
        get_data = self.db_interact(act_data[0], user.id)

        message = f"**{inter.user.display_name}** {act_data[2]} **{
            user.display_name}**\n_{user.display_name} {act_data[4]} {get_data} times_"

        view = InteractableView([])

        # BUG: Remove on_press and let the stupid thing handle it

        def make_button(cfg: ButtonCfg):
            act = get_act(cfg.name)

            async def on_press(btn_inter: discord.Interaction) -> str:
                get_data_ = self.db_interact(act[0], btn_inter.user.id)
                msg = f"**{btn_inter.user.display_name}** {act[2]}"
                if is_interactable(cfg.name):
                    msg += f" **{inter.user.display_name}**\n_{
                        inter.user.display_name} {act[4]} {get_data_} times_"
                return msg

            return buttons(
                cfg.name, on_press, self.neko, act, cfg.emoji, user, cfg.style, view
            )

        btns = [make_button(cfg) for cfg in buttons_cfg if cfg is not None]
        for btn in btns:
            view.add_item(btn)

        msg = await inter.followup.send(
            embed=act_embed(act_name, message, data), view=view
        )
        view.message = msg

    def db_interact(self, act_name, user_id):
        ref = self.bot.db.collection("Nekotina").document(str(user_id))
        doc = ref.get()

        new_total = (doc.to_dict() or {}).get(act_name, 0) + 1 if doc.exists else 1
        ref.set({act_name: new_total}, merge=True)
        return new_total

    @app_commands.command(
        name="lappillow", description="Let someone use your lap as a pillow"
    )
    async def lappillow(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(inter, "lappillow", user, buttons_cfg=[])

    @app_commands.command(name="lurk", description="Lurk around someone")
    async def lurk(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(inter, "lurk", user, buttons_cfg=[])

    @app_commands.command(name="bite", description="Bite someone")
    async def bite(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "bite",
            user,
            buttons_cfg=[
                ButtonCfg("Bite", "🦷"),
                random.choice(punish_buttons),
            ],
        )

    @app_commands.command(name="bonk", description="Bonk someone")
    async def bonk(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "bonk",
            user,
            buttons_cfg=[ButtonCfg("Bonk", "🔨")],
        )

    @app_commands.command(name="blowkiss", description="Blow a kiss to someone")
    async def blowkiss(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "blowkiss",
            user,
            buttons_cfg=[ButtonCfg("Blowkiss", "💨💋")],
        )

    @app_commands.command(name="carry", description="Carry someone")
    async def carry(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(inter, "carry", user, buttons_cfg=[])

    @app_commands.command(name="cuddle", description="Cuddle with someone")
    async def cuddle(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "cuddle",
            user,
            buttons_cfg=[ButtonCfg("Cuddle", "🤗")],
        )

    @app_commands.command(name="handshake", description="Shake hands with someone")
    async def handshake(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "handshake",
            user,
            buttons_cfg=[ButtonCfg("Handshake", "🤝")],
        )

    @app_commands.command(name="handhold", description="Hold hands with someone")
    async def handhold(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "handhold",
            user,
            buttons_cfg=[ButtonCfg("Handhold", "🫱🫲")],
        )

    @app_commands.command(name="highfive", description="High five someone")
    async def highfive(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "highfive",
            user,
            buttons_cfg=[ButtonCfg("Highfive", "🙌")],
        )

    @app_commands.command(name="feed", description="Feed someone")
    async def feed(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "feed",
            user,
            buttons_cfg=[ButtonCfg("Nom", "😋")],
        )

    @app_commands.command(name="hug", description="Hug someone")
    async def hug(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "hug",
            user,
            buttons_cfg=[ButtonCfg("Hug", "🤗")],
        )

    @app_commands.command(name="kick", description="Kick someone")
    async def kick(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "kick",
            user,
            buttons_cfg=[
                ButtonCfg("Kick", "🦵"),
                ButtonCfg("Cry", "😢"),
            ],
        )

    @app_commands.command(name="kabedon", description="Pin someone against wall")
    async def kabedon(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "kabedon",
            user,
            buttons_cfg=[
                ButtonCfg("Kiss", "💖"),
                random.choice(punish_buttons),
            ],
        )

    @app_commands.command(name="kiss", description="Kiss someone")
    async def kiss(
        self, inter: discord.Interaction, user: discord.User, cheeks: bool = False
    ):
        await self.interact_command(
            inter,
            "kiss" if not cheeks else "peck",
            user,
            buttons_cfg=[
                ButtonCfg("Kiss", "💖") if not cheeks else ButtonCfg("Peck", "💖"),
                random.choice(punish_buttons) if not cheeks else None,
            ],
        )

    @app_commands.command(name="pat", description="Pat someone")
    async def pat(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "pat",
            user,
            buttons_cfg=[
                ButtonCfg("Happy", "😊"),
                random.choice(punish_buttons),
            ],
        )

    @app_commands.command(name="poke", description="Poke someone")
    async def poke(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "poke",
            user,
            buttons_cfg=[ButtonCfg("Poke", "👉")],
        )

    @app_commands.command(name="punch", description="Punch someone")
    async def punch(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "punch",
            user,
            buttons_cfg=[ButtonCfg("Punch", "👊")],
        )

    @app_commands.command(name="shoot", description="Shoot someone")
    async def shoot(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "shoot",
            user,
            buttons_cfg=[ButtonCfg("Shoot", "🔫")],
        )

    @app_commands.command(name="shake", description="Shake someone")
    async def shake(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(inter, "shake", user, buttons_cfg=[])

    @app_commands.command(name="slap", description="Slap someone")
    async def slap(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "slap",
            user,
            buttons_cfg=[ButtonCfg("Slap", "🖐️")],
        )

    @app_commands.command(name="tickle", description="Tickle someone")
    async def tickle(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "tickle",
            user,
            buttons_cfg=[ButtonCfg("Laugh", "😂")],
        )

    @app_commands.command(name="wave", description="Wave at someone")
    async def wave(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "wave",
            user,
            buttons_cfg=[ButtonCfg("Wave", "👋")],
        )

    @app_commands.command(name="wink", description="Wink at someone")
    async def wink(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(
            inter,
            "wink",
            user,
            buttons_cfg=[
                ButtonCfg("Wink", "😉"),
                random.choice(punish_buttons),
            ],
        )

    @app_commands.command(name="yeet", description="Yeet someone")
    async def yeet(self, inter: discord.Interaction, user: discord.User):
        await self.interact_command(inter, "yeet", user, buttons_cfg=[])
