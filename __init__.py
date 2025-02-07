import requests
import io
import discord
from discord import app_commands
from discord.ext import commands

with open(".token", "r", encoding="utf-8") as f:
    TOKEN = f.read()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"Logged in as {bot.user} and synced commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")


@bot.tree.command(name="sound", description="Play a sound")
@app_commands.describe(
    name="name",
    message="Name of the sound on the PlSound server."
)
async def sound(ctx, name: str):
    await ctx.defer()

    try:
        response = requests.get(f"https://plsound.wediaklup.de/get/{name}")
        response.raise_for_status()

        filename = response.headers.get("X-Filename")
        data = io.BytesIO(response.content)

        await ctx.respond(file=discord.File(data, filename=filename))

    except requests.exceptions.HTTPError as e:
        await ctx.respond(f"Failed to fetch file: {e}", ephemeral=True)

