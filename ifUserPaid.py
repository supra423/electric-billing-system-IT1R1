import sqlite3
from datetime import datetime
import time
import schedule

'''
To make things clear, this script basically checks if the user has paid
before the due date, if not, the paymentLastBillingPeriod column will get assigned with
paymentThisBillingPeriod, this signifies that the user still has not paid last month's
bill
'''

def job1():
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()
    
    # example, sampleRow = ('May 30, 2025,')
    # fetch a row to determine the due date of the current payment period
    sampleRow = cursor.execute("select dueDate from readings where dueDate != 'N/A'").fetchone()
    currentDatetime = datetime.now().strftime("%B %d, %Y")
   
    # basically this only happens if every single user is new and has not received a bill yet.
    if sampleRow is None:
        print("no valid due date")
        return

    # this basically checks if the current date time is equal to the due date of the payment period
    if sampleRow[0] != currentDatetime:
        return
    
    # now if currentDateTime matches the due date of the current paymnt period
    # fetch all account rows' accountNumber that does not contain a 'N/A' dueDate
    # example, accountFetch = (('1234123412341234,'), ('1212121212121212,'), ... )
    accountFetch = cursor.execute("select accountNumber from readings where dueDate != 'N/A'").fetchall()

    for row in accountFetch:
        # basically, using the account numbers of rows that don't contain a 'N/A' dueDate
        # we will check each account using there accountNumber if their paymentStatus is 'paid' or 'unpaid'
        userPaymentStatusAndPayment = cursor.execute("select paymentStatus, paymentThisBillingPeriod from accounts where accountNumber = ?", (row[0],)).fetchone()
        
        if userPaymentStatusAndPayment[0] == 'unpaid':
            # this is to determine the actual payment made last month

            cursor.execute("update accounts set paymentLastBillingPeriod = ? where accountNumber = ?", (userPaymentStatusAndPayment[1], row[0])) 

    connection.commit()

schedule.every().day.at("00:00").do(job1)

while True:
    schedule.run_pending()

    time.sleep(1)
