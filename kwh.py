import random
import sqlite3
import time

import schedule

"""
This script right here is responsible for simulating that there are actual users in the billing system.

This basically updates the kWh column of each user everyday

It runs once a day and randomly adds 10 to 30 kWh to each active user's `kWh` usage.
This helps mimic real-life usage patterns for testing or simulation purposes.
"""

def job():
    # Connect to SQLite database
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    """     Fetch all account numbers and their current kWh values,
            excluding those that are already marked as 'terminated'     """
    accountFetch = cursor.execute("select accountNumber, kWh from accounts where accountStatus != 'terminated'").fetchall()

    for row in accountFetch:
        # Generate a random kWh usage between 10 and 30 for toda
        addKwh = random.randrange(10, 30)
        # Commit all the updates to the database
        cursor.execute("update accounts set kWh = kWh + ? where accountNumber = ?", (addKwh, row[0]))

    connection.commit() # Commit all the updates to the database

schedule.every().day.at("00:00").do(job)

while True:
    schedule.run_pending()

    time.sleep(1)
