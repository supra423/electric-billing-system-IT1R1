import sqlite3
import time
from datetime import datetime
import schedule

def job():
    if datetime.now().day != 15:
        return

    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    accountFetch1 = cursor.execute("select accountNumber, previousReading, currentReading, previousReadingDate, currentReadingDate from readings").fetchall()

    timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # for example, row = ('1234123412341234', 123, 400, "date", "date")
    for row1 in accountFetch1:
        cursor.execute("update readings set previousReading = ?, previousReadingDate = ? where accountNumber = ?", (row1[2], row1[4], row1[0]))

    accountFetch2 = cursor.execute("select accountNumber, kWh from accounts").fetchall()

    for row2 in  accountFetch2:
        cursor.execute("update readings set currentReading = ?, currentReadingDate = ? where accountNumber = ?", (row2[1], timeStamp, row2[0]))

    connection.commit()

schedule.every().day.at("00:00").do(job)

while True:
    schedule.run_pending()

    time.sleep(1)
