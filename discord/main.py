import credentials

from src.bot import DiscordBot
from src.keep_alive import keep_alive

if __name__ == "__main__":
    try:
        keep_alive()
        bot = DiscordBot()

        bot.run(credentials.TOKEN)
    except KeyboardInterrupt:
        print("Bot Exited!!")
