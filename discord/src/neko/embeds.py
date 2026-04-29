import random

from discord import Embed, Color, ui, ButtonStyle, Interaction, User

colors = [
    Color.red(),
    Color.blue(),
    Color.green(),
    Color.gold(),
    Color.purple(),
    Color.orange(),
    Color.teal(),
    Color.magenta(),
    Color.dark_blue(),
    Color.dark_green(),
    Color.dark_purple(),
    Color.blurple(),
]


def act_embed(name, message, data):
    embed = Embed(
        description=message,
        color=random.choice(colors),
    )

    embed.set_image(url=data.url)
    embed.set_footer(text=f"Anime: {data.anime_name}")

    return embed


class InteractableView(ui.View):
    def __init__(self, buttons: list[ui.Button]):
        super().__init__(timeout=900)

        for btn in buttons:
            self.add_item(btn)

    def disable_all(self):
        for item in self.children:
            item.disabled = True

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(view=self)
        except Exception:
            pass


def buttons(
    name,
    message,
    neko,
    act,
    emoji,
    target: User,
    style: ButtonStyle,
    view: InteractableView,
):
    async def callback(inter: Interaction):
        if inter.user.id != target.id:
            return await inter.response.send_message(
                "❌ These buttons aren't for you!", ephemeral=True
            )

        await inter.response.defer()

        view.disable_all()
        await inter.edit_original_response(view=view)

        data_ = await neko.get_image(act[0])
        await inter.followup.send(embed=act_embed(name, message, data_))

    button = ui.Button(label=name, style=style, custom_id=name.lower(), emoji=emoji)
    button.callback = callback

    return button
