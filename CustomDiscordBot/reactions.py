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

    def parse_message(self, message: discord.Message):
        """
        Parses a message for any lines formatted
        <emoji>: <@role>
        and returns a dict of {emoji:role}
        """
        roles = {}
        for line in message.content.split("\n"):
            try:
                emoji, role = line.split(": ")
                roles[emoji] = role
            except ValueError:
                # There wern't two to unpack
                continue
        return roles



    @commands.Cog.listener("on_raw_reaction_add")
    async def user_reacted(self, payload: discord.RawReactionActionEvent):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        user = payload.member
        self.parse_message(message)


    @commands.Cog.listener("on_raw_reaction_remove")
    async def user_unreacted(self, payload: discord.RawReactionActionEvent):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        user = payload.member
        self.parse_message(message)


