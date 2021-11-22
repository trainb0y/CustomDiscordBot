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

    @commands.Cog.listener("on_raw_reaction_add")
    async def user_reacted(self, payload: discord.RawReactionActionEvent):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        user = payload.member
        print(f"{user.name} reacted to {message} with {payload.emoji}")
