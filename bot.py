import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

# helper.py
from helper import *

# get environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

ADDR_LAT = os.getenv('ADDR_LAT')
ADDR_LONG = os.getenv('ADDR_LONG')

URL_RAIN = os.getenv('URL_RAIN')

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