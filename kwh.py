import random
import sqlite3
import time

import schedule

connection = sqlite3.connect('database.s3db')
cursor = connection.cursor()

def job():
    kWh = random.randrange(10, 30)
    cursor.execute('update accounts set kWh = kWh + (?)', (kWh,))
    connection.commit()
    print("Updated new kWh for all users")

schedule.every().day.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
