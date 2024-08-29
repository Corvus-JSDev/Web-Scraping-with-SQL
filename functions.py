import requests
import selectorlib

def scrape(url):
	"""Scrape the source page from the given URL"""

	try:
		response = requests.get(url)
		data = response.text
		return data

	except requests.RequestException as err:
		print(f'ERROR: {err}')