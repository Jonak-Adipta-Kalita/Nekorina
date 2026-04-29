import credentials
import src.bot as bot_

from src.doomsdayclock.timestamp import (
    write_stored_timestamp,
    read_stored_timestamp,
    parse_timestamp,
    format_timestamp,
)


class OnLoad:
    def __init__(self, bot: bot_.DiscordBot):
        self.bot = bot

    async def on_load_check_change(self):
        latest = self.bot.latest_message_ref.get().to_dict()
        if not latest:
            return

        stored = read_stored_timestamp()

        if stored is None:
            write_stored_timestamp(latest["timestamp"])
            return

        latest_ts = parse_timestamp(latest["timestamp"])

        if latest_ts <= stored:
            return

        snapshot = self.bot.messages_ref.stream()
        all_messages = [{"id": doc.id, **doc.to_dict()} for doc in snapshot]
        new_messages = [
            m
            for m in all_messages
            if m["id"] != "latest" and parse_timestamp(m["timestamp"]) > stored
        ]
        new_messages.sort(key=lambda m: parse_timestamp(m["timestamp"]))

        for msg in new_messages:
            await self.dm_user(msg)

        write_stored_timestamp(latest["timestamp"])

    def on_snapshot(self, doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == "MODIFIED":
                data = change.document.to_dict()
                self.bot.loop.create_task(self.dm_user(data))

    async def dm_user(self, data: dict):
        change_user = data["user"]
        dm_user_id = None
        if change_user == credentials.BRO_NAME:
            dm_user_id = int(credentials.SIS_ID)
        elif change_user == credentials.SIS_NAME:
            dm_user_id = int(credentials.BRO_ID)

        if dm_user_id is None:
            return

        dm_user = await self.bot.fetch_user(dm_user_id)
        await dm_user.send(f"Clock updated by {change_user} @ {
            format_timestamp(data['timestamp'])}!")
        write_stored_timestamp(data["timestamp"])
