from pprint import pp
import requests
import selectorlib
import smtplib, ssl
import os
from email.message import EmailMessage
from dotenv import load_dotenv
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
		obj_value = {
			"band": array_value[0],
			"location": array_value[1],
			"date": array_value[2]
		}
		# The reason for having a string value is for saving data, and the array value is to have control over formatting to make it look pretty when sending the email.
		return {"string_value": string_value, "array_value": array_value, "obj_value": obj_value}


	return value.lower()  # "no upcoming tours"



load_dotenv()
EMAIL_USR = os.getenv("EMAIL_USR")
EMAIL_PW = os.getenv("EMAIL_PW")
def send_email(message):
	msg = EmailMessage()
	msg['Subject'] = "New Music Event!"
	msg['From'] = EMAIL_USR
	msg['To'] = EMAIL_USR
	msg.set_content(f"There has been a new event detected.\n\n{message['band']} is playing in {message['location']} on {message['date']}")

	with smtplib.SMTP("smtp.gmail.com", 587) as gmail:
		gmail.ehlo()
		gmail.starttls()
		gmail.login(EMAIL_USR, EMAIL_PW)
		gmail.sendmail(EMAIL_USR, EMAIL_USR, msg.as_string())

	print(f"Email sent: {message}")





if __name__ == "__main__":
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

		# send_email(extract["obj_value"])










