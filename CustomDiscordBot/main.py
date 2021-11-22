import os, logging, reactions
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
bot = commands.Bot(command_prefix="$")

load_dotenv()
bot.add_cog(reactions.Reactions(bot))
bot.run(os.getenv("DISCORD_TOKEN"))
