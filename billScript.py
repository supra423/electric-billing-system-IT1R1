import sqlite3
import time
from datetime import datetime
import schedule

def job():
    #if datetime.now().day != 15:
    #    return

    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    accountFetch1 = cursor.execute("select accountNumber, previousReading, currentReading from readings").fetchall()
    
    # for example, row = ('1234123412341234', 123, 400)
    for row1 in accountFetch1:
        cursor.execute("update readings set previousReading = ? where accountNumber = ?", (row1[2], row1[0]))

    accountFetch2 = cursor.execute("select accountNumber, kWh from accounts").fetchall()

    for row2 in  accountFetch2:
        cursor.execute("update readings set currentReading = ? where accountNumber = ?", (row2[1], row2[0]))

    connection.commit()

job()
