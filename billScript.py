import sqlite3
import time
from datetime import datetime, timedelta
import schedule

def job1():
    if datetime.now().day != 20:
        return

    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    accountFetch1 = cursor.execute("select accountNumber, previousReading, currentReading, previousReadingDate, currentReadingDate from readings").fetchall()

    timeStamp = datetime.now().strftime("%B %d, %Y")
    billDueDate = datetime.now() + timedelta(days = 15)
    formattedDueDate = billDueDate.strftime("%B %d, %Y")

    # for example, row1 = ('1234123412341234', 123, 400, "date", "date", "dueDate")
    for row1 in accountFetch1:
        cursor.execute("update readings set previousReading = ?, previousReadingDate = ? where accountNumber = ?", (row1[2], row1[4], row1[0]))
    

    accountFetch2 = cursor.execute("select accountNumber, kWh from accounts").fetchall()

    for row2 in  accountFetch2:
        cursor.execute("update readings set currentReading = ?, currentReadingDate = ?, dueDate = ? where accountNumber = ?", (row2[1], timeStamp, formattedDueDate, row2[0]))

    connection.commit()

def job2():
    if datetime.now().day != 21:
        return

    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    pendingBalanceCalculate = cursor.execute("select accountNumber, previousReading, currentReading from readings").fetchall()

    for reading in pendingBalanceCalculate:
        # 10 pesos per kWh and 12% value added tax
        totalPaymentWithoutVat = 10 * (reading[2] - reading[1])
        addVat = totalPaymentWithoutVat * 0.12
        totalPaymentWithVat = addVat + totalPaymentWithoutVat
        
        cursor.execute("update accounts set pendingBalance = pendingBalance + ? where accountNumber = ?", (totalPaymentWithVat, reading[0]))
    
    connection.commit()

schedule.every().day.at("00:00").do(job1)
schedule.every().day.at("00:00").do(job2)

while True:
    schedule.run_pending()

    time.sleep(1)
