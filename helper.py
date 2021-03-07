# returns JSON from GET request
def getJSON(URL):
	from requests import get
	json = get(URL).json()
	return json

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