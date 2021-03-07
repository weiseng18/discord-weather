# returns JSON from GET request
def getJSON(URL):
	from requests import get
	json = get(URL).json()
	return json