import discord, logging
from discord.ext import commands


class Reactions(commands.Cog):
    """
    Handles reaction roles

    Any user reacting to a message that contains one or more lines with
    emoji: @role
    receives or removes the role upon reacting with that emoji
    """

    def __init__(self, bot: commands.Bot):
        super().__init__()  # Just to be safe
        self.bot = bot
        self.reaction_role_pairs = {}

    def parse_message(self, message: discord.Message) -> [(str, discord.Role)]:
        """
        Parses a message for any lines formatted
        <emoji>: <@role>
        and returns a dict of {emoji:role}
        """
        logging.debug(f"Attempting to parse message {message} for roles")
        roles = []
        for line in message.content.split("\n"):
            try:
                emoji, role = line.split(":")
                emoji = emoji.strip()  # Remove any whitespace
                role = role.strip().replace("<@&", "").replace(">", "")  # There's probably a better way to parse this
                role = message.guild.get_role(int(role))  # Attempt to get the Role object
                if role is None: continue  # If it didn't find one, move on
                logging.debug(f"Found role {role} at emoji {emoji}")
                roles.append((emoji, role))

            except ValueError:
                # There weren't two to unpack, probably
                continue

        logging.debug(f"Returning {roles}")
        return roles

    @commands.Cog.listener("on_raw_reaction_add")
    async def user_reacted(self, payload: discord.RawReactionActionEvent):
        """
        Give the specified role to a user when they react to a role message
        """
        emoji_role_pairs = self.parse_message(
            await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id))
        for pair in emoji_role_pairs:
            if str(payload.emoji) == pair[0]:  # Str it so custom emoji should work
                await payload.member.add_roles(pair[1],reason="Reaction roles")
                logging.info(f"Gave role {pair[1]} to user {payload.member.name}")

    @commands.Cog.listener("on_raw_reaction_remove")
    async def user_unreacted(self, payload: discord.RawReactionActionEvent):
        """
        Remove the specified role from a user when they remove their reaction from a role message
        """
        emoji_role_pairs = self.parse_message(
            await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id))
        # Payload.member doesn't exist for on_raw_reaction_remove, see
        # https://stackoverflow.com/questions/64494476/discord-py-on-raw-reaction-remove-member-not-found-remove-role-on-reaction-remo
        guild = await self.bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        for pair in emoji_role_pairs:
            if str(payload.emoji) == pair[0]:
                await member.remove_roles(pair[1],reason="Reaction roles")
                logging.info(f"Removed role {pair[1]} from user {member.name}")
