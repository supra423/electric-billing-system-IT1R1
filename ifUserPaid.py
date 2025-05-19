import sqlite3
from datetime import datetime, timedelta
import time
import schedule

'''
To make things clear, this script has 2 functions.

the second function (job1) runs in the recorded dueDate 
what it does is that it not only checks the paymentStatus of each user but also check if the user has
unpaid balance from last month's bill by checking if the paymentLastBillingPeriod is greater than 0
meaning that they haven't paid for straight 2 billing periods. If such a user exists, give them 2 days
to comply by marking them as 'almost terminated' before marking their account as 
'terminated' which basically just 'freezes the account'


the second function (job2) basically checks if the user has paid
before the due date (by checking the payment status if it is 'paid' or 'unpaid'), 
if not, the paymentLastBillingPeriod column will get appended with
paymentThisBillingPeriod, this signifies that the user still has not paid last month's
bill

the third function basically checks if there is still a user with the 'almost terminated' status,
if such a user exists and it is already past the disconnection date, then mark that user as 'terminated'

these functions basically run everyday trying to check if it is the due date or if it is the disconnectionDate
(disconnectionDate is basically the 48 hour last chance given to the user to comply a payment)
'''

def job1():
    
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()
   
    # Fetch one reading with a valid due date (not 'N/A')
    sampleRow = cursor.execute("select dueDate from readings where dueDate != 'N/A'").fetchone()

    # If no due date found, exit
    if sampleRow is None:
        return

    # Due date string into a datetime object
    dateObject = datetime.strptime(sampleRow[0], "%B %d, %Y")
    currentDatetime = datetime.now().strftime("%B %d, %Y")

     # Calculate the disconnection date (3 days after due date)
    newDate = dateObject + timedelta(days = 3)
    newDateFormatted = newDate.strftime("%B %d, %Y")
 
    # If today is not the due date, do nothing
    if sampleRow[0] != currentDatetime:
        return

    """     Get accounts that are unpaid, have unpaid balance from last month,
            unpaid this billing period, and were marked as not paid last month     """
    accountFetch = cursor.execute("select accountNumber from accounts where paymentStatus = 'unpaid' AND paymentLastBillingPeriod != 0 AND paymentThisBillingPeriod != 0 AND paidLastMonth = 'false'").fetchall()

    # For each account found, mark as 'almost terminated' and set disconnection date
    for row in accountFetch:

        accountAlmostTermination = cursor.execute("update accounts set accountStatus = 'almost terminated' where accountNumber = ?", (row[0],))
        accountDisconnectionDateUpdate = cursor.execute("update readings set disconnectionDate = ? where accountNumber = ?", (newDateFormatted, row[0]))

    connection.commit()

def job2():
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    # Fetch one reading with a valid due date
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
        userPaymentStatusAndPayment = cursor.execute("select paymentStatus, paymentThisBillingPeriod, pendingBalance, paidLastMonth from accounts where accountNumber = ?", (row[0],)).fetchone()
        
        if userPaymentStatusAndPayment[0] == 'unpaid' and userPaymentStatusAndPayment[3] == 'true':

            cursor.execute("update accounts set paymentLastBillingPeriod = paymentLastBillingPeriod + ? where accountNumber = ?", (userPaymentStatusAndPayment[1], row[0])) 
            # Reset current billing amount since it's added to last billing period balance
            cursor.execute("update accounts set paymentThisBillingPeriod = 0 where paymentStatus = ? AND accountNumber = ?", (userPaymentStatusAndPayment[0], row[0]))
            cursor.execute("update accounts set paidLastMonth = 'false' where paymentStatus = ? AND accountNumber = ?", (userPaymentStatusAndPayment[0], row[0]))

    connection.commit()

def job3():
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    # Fetch one reading with a valid disconnection date
    sampleRow = cursor.execute("select disconnectionDate from readings where disconnectionDate != 'N/A'").fetchone()

    # If no disconnection date found, exit
    if sampleRow is None:
        return

    dateObject = datetime.strptime(sampleRow[0], "%B %d, %Y")
    newDate = dateObject + timedelta(days = 3)
    newDateFormatted = newDate.strftime("%B %d, %Y")
   
    # if there are no rows that contain a disconnection date
    currentDatetime = datetime.now().strftime("%B %d, %Y")

    # Only proceed if today is the disconnection date
    # if today is not disconnection date
    if sampleRow[0] != currentDatetime:
        return

    # Fetch all niggaz marked 'almost terminated'
    accountFetch = cursor.execute("select accountNumber from accounts where accountStatus = 'almost terminated'").fetchall()

    # Mark these niggaz as 'terminated' (account freeze?)
    for row in accountFetch:
        accountTermination = cursor.execute("update accounts set accountStatus = 'terminated' where accountNumber = ?", (row[0],))

    connection.commit()

schedule.every().day.at("00:00").do(job1)
schedule.every().day.at("00:01").do(job2)
schedule.every().day.at("00:02").do(job3)

while True:
    schedule.run_pending()

    time.sleep(1)
