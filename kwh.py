import random
import sqlite3
import time

import schedule

def job():
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()
    accountFetch = cursor.execute("select accountNumber, kWh from accounts").fetchall()

    for row in accountFetch:
        addKwh = random.randrange(10, 30)
        cursor.execute("update accounts set kWh = kWh + ? where accountNumber = ?", (addKwh, row[0]))

    connection.commit()

schedule.every().day.at("00:00").do(job)

while True:
    schedule.run_pending()

    time.sleep(1)
