import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

# get environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# bot constants
prefix = "!"
client = commands.Bot(command_prefix = prefix)

# ---------------
# bot events
# ---------------

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)