import requests
import selectorlib

# Pretending to be a browser
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
def scrape(url):
	"""Scrape the source page from the given URL"""

	try:
		response = requests.get(url, HEADER)
		data = response.text
		return data

	except requests.RequestException as err:
		print(f'ERROR: {err}')