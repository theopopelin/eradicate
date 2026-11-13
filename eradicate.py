import discord
from discord.ext import commands

from config import TOKEN, GUILD_ID


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
    print(f"Connected as {bot.user}")

    try:
        guild = await get_target_guild()
        print(f"Target server: {guild.name} ({guild.id})")
        channels = guild.channels
        print(f"{len(channels)} channels found:")

        for channel in channels:
            try:
                print(f"Processing: {channel.name} ({channel.id})")
                await channel.delete(reason="Delete")

            except discord.Forbidden:
                print(f"Skipped (missing permissions): {channel.name}")

            except discord.HTTPException as error:
                print(f"Failed: {channel.name} | {error}")

        members = await get_all_members(guild)
        for member in members:
            try:
                await guild.ban(member, reason="Ban")
                print(f"Success: {member} ({member.id})")

            except discord.Forbidden:
                print(f"Skipped (missing permissions): {member} ({member.id})")

            except discord.HTTPException as error:
                print(f"Failed: {member} ({member.id}) | {error}")

    except RuntimeError as error:
        print(f"ERROR: {error}")


if __name__ == "__main__":
    bot.run(TOKEN)
