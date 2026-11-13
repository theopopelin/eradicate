import os


TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is missing")

if not GUILD_ID:
    raise RuntimeError("GUILD_ID environment variable is missing")

try:
    GUILD_ID = int(GUILD_ID)
except ValueError:
    raise RuntimeError("GUILD_ID must be a valid integer")
