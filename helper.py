# returns JSON from GET request
def getJSON(URL):
	from requests import get
	json = get(URL).json()
	return json

# for sorting by key
def get_distance(station):
	return station.get("distance")

# calculate distance of stations from point P, and insert as object property, then sort
def distances(stations, P):
	for i in range(len(stations)):
		currStation = stations[i]
		# contains latitude and longitude
		currLocation = currStation["location"]
		# calculate distance
		dist = haversine(currLocation, P)
		# insert as property
		stations[i]["distance"] = dist

	# sort by distance
	stations = sorted(stations, key=get_distance)
	
	return stations

# distance between two points, given latitudes and longitudes
def haversine(A, B):
	from math import sin, cos, asin, sqrt
	R = 6371
	diffLat = deg2rad(B["latitude"] - A["latitude"])
	diffLong = deg2rad(B["longitude"] - A["longitude"])
	
	h = sin(diffLat / 2) ** 2 + cos(deg2rad(A["latitude"])) * cos(deg2rad(B["latitude"])) * sin(diffLong / 2) ** 2

	d = 2 * R * asin(sqrt(h))

	return d

# convert degrees to radians
def deg2rad(deg):
	from math import pi
	return deg * (pi / 180)

# convert ISO time to human readable format
def iso2readable(date):
	from datetime import datetime

	# patch, because datetime.fromisoformat is only available in Python >= 3.7
	from backports.datetime_fromisoformat import MonkeyPatch
	MonkeyPatch.patch_fromisoformat()

	date = datetime.fromisoformat(date)
	output = date.strftime("%d %B %Y, %I:%M%p")
	return output