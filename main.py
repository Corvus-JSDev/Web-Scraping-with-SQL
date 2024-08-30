from pprint import pp
from functions import *
import sqlite3 as sql

URL = "https://programmer100.pythonanywhere.com/tours/"

scraper = scrape(URL)
extract = extract(scraper)


if extract != "no upcoming tours":
	connection = sql.connect("SQL_Database.db")
	cursor = connection.cursor()
	band, location, date = extract["array_value"]

	# Read the contents of the database and find if there is a matching row
	cursor.execute("SELECT * FROM events WHERE band=? AND location=? AND date=?", (band, location, date))
	sql_data = cursor.fetchall()

	if sql_data == []:
		# Write to the db, so you don't get two emails for the same event
		cursor.execute("INSERT INTO events VALUES(?,?,?)", (band, location, date))
		connection.commit()

		send_email(extract["obj_value"])

	else:
		print("An alert for this event has already been sent.")

else:
	print("No Upcoming Tours :(")