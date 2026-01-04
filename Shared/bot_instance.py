from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.message_content = True

cpu_discord_bot = commands.Bot(command_prefix="/", intents=intents)
