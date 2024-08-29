from pprint import pp
from functions import *

URL = "https://programmer100.pythonanywhere.com/tours/"

scraper = scrape(URL)
extract = extract(scraper)
pp(extract)

# Read the contents of the data file
with open("data.txt", "r") as file:
	file_contents = file.read()

if extract != "no upcoming tours" and extract["string_value"] not in file_contents:
	# Store the data in a file, so you don't get two emails for the same event
	with open("data.txt", "a") as file:
		file.write(f"{extract['string_value']}\n")

	send_email(extract["array_value"])
