import discord
import credentials
import firebase_admin
import firebase_admin.credentials
import firebase_admin.firestore

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
        self.db.collection("Messages").document("latest").on_snapshot(self.on_snapshot)

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

    def on_snapshot(self, doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == "MODIFIED":
                data = change.document.to_dict()
                self.loop.create_task(self.dm_user(data))

    async def dm_user(self, data: dict):
        change_user = data["user"]
        dm_user_id = None

        if change_user == credentials.BRO_NAME:
            dm_user_id = int(credentials.SIS_ID)
        elif change_user == credentials.SIS_NAME:
            dm_user_id = int(credentials.BRO_ID)

        dm_user = await self.fetch_user(dm_user_id)

        await dm_user.send(f"Clock updated by {change_user}!")
