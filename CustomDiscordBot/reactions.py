import discord, logging
from discord.ext import commands


class Reactions(commands.Cog):
    """
    Handles reaction roles
    """

    def __init__(self, bot: commands.Bot):
        super().__init__()  # Just to be safe
        self.bot = bot
        self.reaction_role_pairs = {}

    @commands.Cog.listener("on_reaction_add")
    async def user_reacted(self, reaction: discord.Reaction, user: discord.User):
        print(f"{user.name} reacted to {reaction.message} with {reaction.emoji}")
