import sqlite3
from datetime import datetime, timedelta
import time
import schedule

'''
To make things clear, this script has 2 functions.
the first function (job1) basically checks if the user has paid
before the due date (by checking the payment status if it is 'paid' or 'unpaid'), 
if not, the paymentLastBillingPeriod column will get assigned with
paymentThisBillingPeriod, this signifies that the user still has not paid last month's
bill

the second function (job2) also runs almost the same time as the first function but instead, 
what it does is that it not only checks the paymentStatus of each user but also check if the user has
unpaid balance from last month's bill by checking if the paymentLastBillingPeriod is greater than 0
meaning that they haven't paid for straight 2 billing periods. If such a user exists, give them 2 days
to comply by marking them as 'almost terminated' before marking their account as 
'terminated' which basically just 'freezes the account'

these functions basically run everyday trying to check if it is the due date or if it is the disconnectionDate
(disconnectionDate is basically the 48 hour last chance given to the user to comply a payment)
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
    
    # now if currentDatetime matches the due date of the current paymnt period
    # fetch all account rows' accountNumber that does not contain a 'N/A' dueDate
    # example, accountFetch = (('1234123412341234,'), ('1212121212121212,'), ... )
    accountFetch = cursor.execute("select accountNumber from readings where dueDate != 'N/A'").fetchall()

    for row in accountFetch:
        # basically, using the account numbers of rows that don't contain a 'N/A' dueDate
        # we will check each account using there accountNumber if their paymentStatus is 'paid' or 'unpaid'
        userPaymentStatusAndPayment = cursor.execute("select paymentStatus, paymentThisBillingPeriod, pendingBalance from accounts where accountNumber = ?", (row[0],)).fetchone()
        
        if userPaymentStatusAndPayment[0] == 'unpaid':

            cursor.execute("update accounts set paymentLastBillingPeriod = ? where accountNumber = ?", (userPaymentStatusAndPayment[1], row[0])) 
            cursor.execute("update accounts set paymentThisBillingPeriod = 0 where paymentStatus = ? AND accountNumber = ?", (userPaymentStatusAndPayment[0], row[0]))
        
    connection.commit()

def job2():
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()
   
    sampleRow = cursor.execute("select dueDate from readings where dueDate != 'N/A'").fetchone()

    if sampleRow is None:
        return

    dateObject = datetime.strptime(sampleRow[0], "%B %d, %Y")
    currentDatetime = datetime.now().strftime("%B %d, %Y")

    newDate = dateObject + timedelta(days = 3)
    newDateFormatted = newDate.strftime("%B %d, %Y")
 
    if sampleRow[0] != currentDatetime:
        return

    accountFetch = cursor.execute("select accountNumber from accounts where paymentStatus = 'unpaid' AND paymentLastBillingPeriod != 0 AND paymentThisBillingPeriod != 0").fetchall()

    for row in accountFetch:

        accountAlmostTermination = cursor.execute("update accounts set accountStatus = 'almost terminated' where accountNumber = ?", (row[0],))
        accountDisconnectionDateUpdate = cursor.execute("update readings set disconnectionDate = ?", (newDateFormatted,))
    connection.commit()


def job3():
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    sampleRow = cursor.execute("select disconnectionDate from readings where disconnectionDate != 'N/A'").fetchone()

    if sampleRow is None:
        return

    dateObject = datetime.strptime(sampleRow[0], "%B %d, %Y")
    newDate = dateObject + timedelta(days = 3)
    newDateFormatted = newDate.strftime("%B %d, %Y")
   
    # if there are no rows that contain a disconnection date
    currentDatetime = datetime.now().strftime("%B %d, %Y")

    # if today is not disconnection date
    if sampleRow[0] != currentDatetime:
        return

    accountFetch = cursor.execute("select accountNumber from accounts where accountStatus = 'almost terminated'").fetchall()

    for row in accountFetch:
        accountTermination = cursor.execute("update accounts set accountStatus = 'terminated' where accountNumber = ?", (row[0],))

    connection.commit()

schedule.every().day.at("00:00").do(job1)
schedule.every().day.at("00:01").do(job2)
schedule.every().day.at("00:02").do(job3)

while True:
    schedule.run_pending()

    time.sleep(1)
