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

# ---------------
# bot commands
# ---------------

@client.command(
	help="placeholder",
	brief="placeholder"
)
async def check(ctx):
	# pull data from data.gov.sg
	json = getJSON(URL_RAIN)

	# put data into meaningful variables
	stationInfo = json["metadata"]["stations"]
	UNIT = json["metadata"]["reading_unit"]
	readings = json["items"][0]["readings"]
	LAST_UPDATE = json["items"][0]["timestamp"]

	# sort stations by distance from location specified in .env
	P = {"latitude": float(ADDR_LAT), "longitude": float(ADDR_LONG)}
	sortedStationInfo = distances(stationInfo, P)

	# get 3 closest stations
	closestStations = sortedStationInfo[:3]

	# print last update timestamp
	output = "Last updated at: {0}".format(LAST_UPDATE)
	await ctx.channel.send(output)

	# get rainfall info
	for station in closestStations:
		ID = station["id"]
		NAME = station["name"]
		DISTANCE = station["distance"]
		RAINFALL = [reading for reading in readings if reading.get("station_id") == ID][0]["value"]

		output = "Station at {0}, {1:.2f} km away, has reading {2} {3}".format(NAME, DISTANCE, RAINFALL, UNIT)
		await ctx.channel.send(output)

client.run(TOKEN)