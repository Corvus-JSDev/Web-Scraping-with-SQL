import requests
import selectorlib
URL = "https://programmer100.pythonanywhere.com/tours/"

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
		


def extract(source):
	"""Extract data from a source file"""

	extractor = selectorlib.Extractor.from_yaml_file("source.yaml")
	value = extractor.extract(source)["tours"]

	if value != "No upcoming tours":
		string_value = value
		array_value = [item.strip() for item in value.split(",")]
		return {"string_value": string_value, "array_value": array_value}

	return value.lower()  # "no upcoming tours"



def send_email(message):
	"""Send an email"""

	print("Email Sent")




if __name__ == "__main__":
	scraper = scrape(URL)
	extract = extract(scraper)

	# Read the contents of the data file
	with open("data.txt", "r") as file:
		file_contents = file.read()

	if extract != "no upcoming tours" and extract["string_value"] not in file_contents:
		# Store the data in a file, so you don't get two emails for the same event
		with open("data.txt", "a") as file:
			file.write(f"{extract['string_value']}\n")

		send_email(extract)










