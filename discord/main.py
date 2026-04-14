import credentials

from src.bot import DiscordBot

if __name__ == "__main__":
    try:
        bot = DiscordBot()

        bot.run(credentials.TOKEN)
    except KeyboardInterrupt:
        print("Bot Exited!!")
