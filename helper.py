# returns JSON from GET request
def getJSON(URL):
	from requests import get
	json = get(URL).json()
	return json

# convert degrees to radians
def deg2rad(deg):
	from math import pi
	return deg * (pi / 180)