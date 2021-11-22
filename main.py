import os, discord
from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="$")

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.getenv("DISCORD_TOKEN"))
