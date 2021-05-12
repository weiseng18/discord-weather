import os
from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks

# helper.py
from helper import *

# get environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

ADDR_LAT = os.getenv('ADDR_LAT')
ADDR_LONG = os.getenv('ADDR_LONG')

# bot constants
prefix = "!"
client = commands.Bot(command_prefix = prefix)

# last update of forecast
LAST_UPDATE_FORECAST = 0

# ---------------
# bot events
# ---------------

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    forecast.start()

# ---------------
# bot commands
# ---------------

@client.command(
	help="placeholder",
	brief="placeholder"
)
async def check(ctx):
	URL_RAIN = "https://api.data.gov.sg/v1/environment/rainfall"

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
	output = "Last updated at: {0}\n".format(LAST_UPDATE)

	# get rainfall info
	for station in closestStations:
		ID = station["id"]
		NAME = station["name"]
		DISTANCE = station["distance"]
		RAINFALL = [reading for reading in readings if reading.get("station_id") == ID][0]["value"]

		output += "Station at {0}, {1:.2f} km away, has reading {2} {3}\n".format(NAME, DISTANCE, RAINFALL, UNIT)

	await ctx.channel.send(output)

# ---------------
# bot functionality
# ---------------

@tasks.loop(minutes=1.0)
async def forecast():
	global client
	global LAST_UPDATE_FORECAST

	URL_FORECAST = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"

	json = getJSON(URL_FORECAST)

	# put data into meaningful variables
	validity = json["items"][0]["valid_period"]
	forecasts = json["items"][0]["forecasts"]
	update = json["items"][0]["update_timestamp"]

	# check if there has been a change in data
	if update == LAST_UPDATE_FORECAST:
		return

	LAST_UPDATE_FORECAST = update

	# print last update timestamp
	output = "Last updated at: {0}\nForecast for next 2 hours:\n".format(iso2readable(LAST_UPDATE_FORECAST))

	# check if there is rain
	hasRain = False
	rainTexts = ["Rain", "Shower"]

	# locations interested in
	locations = ["Punggol", "Sengkang"]
	for location in locations:
		FORECAST = [forecast for forecast in forecasts if forecast.get("area") == location][0]["forecast"]
		if any(text in FORECAST for text in rainTexts):
			hasRain = True
		output += "{0}: {1}\n".format(location, FORECAST)

	# if there is rain, ping everyone
	if hasRain:
		output += "@everyone\n"

	# search for channel
	for guild in client.guilds:
		channel = discord.utils.get(guild.text_channels, name="weather")
		await channel.send(output)


client.run(TOKEN)
