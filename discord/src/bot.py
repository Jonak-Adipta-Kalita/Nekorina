import discord
import credentials
import firebase_admin
import firebase_admin.credentials
import firebase_admin.firestore
import src.doomsdayclock.onload

from discord.ext import commands
from discord import app_commands


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all(),
            help_command=None,
            description="Discord Interface for https://doomsday-clock-for-archie.vercel.app/",
            allowed_contexts=app_commands.AppCommandContext(
                guild=True, dm_channel=True, private_channel=True
            ),
            allowed_installs=app_commands.AppInstallationType(guild=False, user=True),
        )

    async def setup_hook(self):
        creds = {
            "type": credentials.FIREBASE_TYPE,
            "project_id": credentials.FIREBASE_PROJECT_ID,
            "private_key_id": credentials.FIREBASE_PRIVATE_KEY_ID,
            "private_key": credentials.FIREBASE_PRIVATE_KEY,
            "client_email": credentials.FIREBASE_CLIENT_EMAIL,
            "client_id": credentials.FIREBASE_CLIENT_ID,
            "auth_uri": credentials.FIREBASE_AUTH_URI,
            "token_uri": credentials.FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": credentials.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": credentials.FIREBASE_CLIENT_X509_CERT_URL,
        }
        (
            firebase_admin.initialize_app(
                credential=firebase_admin.credentials.Certificate(creds)
            )
            if not len(firebase_admin._apps)
            else firebase_admin.get_app()
        )

        self.db = firebase_admin.firestore.client()

        self.messages_ref = self.db.collection("Messages")
        self.latest_message_ref = self.messages_ref.document("latest")

        self.doomsday_onload = src.doomsdayclock.onload.OnLoad(self)
        self.latest_message_ref.on_snapshot(self.doomsday_onload.on_snapshot)
        await self.doomsday_onload.on_load_check_change()

        await self.load_extension("src.doomsdayclock.commands")
        await self.load_extension("src.neko.commands")

    async def on_connect(self):
        print("Bot Connected!")

        # TODO: Not Work

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                name="Watching over the cute siblinghood",
                type=discord.ActivityType.watching,
            ),
        )

    async def on_disconnect(self):
        print("Bot is Disconnected!!")

    async def on_ready(self):
        await self.tree.sync()

    def authenticate(self, inter: discord.Interaction) -> (bool, str, bool):
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
