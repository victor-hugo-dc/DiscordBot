import discord
from discord.ext import commands
import requests
import json
import atexit
import os

client = commands.Bot(command_prefix = '!', case_insensitive=True)
# Add module file names
modules = []

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("working"))

@client.event
async def on_message(message):
    await client.process_commands(message)

@client.command()
async def load(extension : str):
    try:
        client.load_extension(extension)
    except (AttributeError, ImportError) as e:
        await client.say(f"```py\n{type(e).__name__}: {str(e)}\n```")
        return
    await client.say(f"{extension} loaded.")

@client.command()
async def unload(extension : str):
    client.unload_extension(extension)
    await bot.say(f"{extension} unloaded.")

def load_all():
    client.load_extension(extension) for extension in modules

@atexit
def end():
    client.close()

load_all()
client.run(os.environ["TOKEN"])
