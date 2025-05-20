import sqlite3 #SQLite database
import time #For sleep control
from datetime import datetime, timedelta # For date and time operations
import schedule # For scheduling tasks
import json # For reading the kWh rate from a config file

"""

This script has two functions that are scheduled to run in the 20th and 21st day, respectively

in the 1st function, think of it as reading the user's meter, this function basically determines the kwh
consumption of every user by taking the currentReading value column and assigning it to previousReading column
while the currentReading's value gets assigned by kWh column from the accounts table so basically

previousReading = currentReading
and then
currentReading = kWh (from accounts table)

same goes for the readings dates:
previousReadingDate = currentReadingDate
currentReadingDate = datetime.now()

and then the due date is assigned 10 days ahead the datetime.now()

in the 2nd function, the readings are then calculated for each user and generates a bill for every user 
this then sets every account's paymentStatus to 'unpaid' and their notifications viewed column to 'false'

"""

def job1():
    # Exit if today is not the 20th
    if datetime.now().day != 20:
        return

    # Connect SQLite database
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    # Fetch all accounts with their reading data
    accountFetch1 = cursor.execute("select accountNumber, previousReading, currentReading, previousReadingDate, currentReadingDate from readings").fetchall()

    # Get current date as timestamp string (e.g., "May 20, 2025")
    timeStamp = datetime.now().strftime("%B %d, %Y")
    # Calculate due date (10 days after now)
    billDueDate = datetime.now() + timedelta(days = 10)
    formattedDueDate = billDueDate.strftime("%B %d, %Y")

    # Loop through all account readings
    # for example, row1 = ('1234123412341234', 123, 400, "date", "date", "dueDate")
    for row1 in accountFetch1:

        # first check the account if it is terminated or not
        accountStatusCheck1 = cursor.execute("select accountStatus from accounts where accountNumber = ?", (row1[0],)).fetchone()

        # If active, move current reading to previous
        if accountStatusCheck1[0] == 'active':
            cursor.execute("update readings set previousReading = ?, previousReadingDate = ? where accountNumber = ?", (row1[2], row1[4], row1[0]))
        else:
            continue # Skip if account is not active

    # Fetch the latest kWh values from accounts table
    accountFetch2 = cursor.execute("select accountNumber, kWh from accounts").fetchall()

    # Update the current reading with the new kWh and set new reading date and due date
    for row2 in accountFetch2:

        accountStatusCheck2 = cursor.execute("select accountStatus from accounts where accountNumber = ?", (row2[0],)).fetchone()

        if accountStatusCheck2[0] == 'active':
            cursor.execute("update readings set currentReading = ?, currentReadingDate = ?, dueDate = ? where accountNumber = ?", (row2[1], timeStamp, formattedDueDate, row2[0]))
        else:
            continue

    # Save all changes to the database
    connection.commit()

def job2():
    # Exit if today is not the 21st
    if datetime.now().day != 21:
        return

    # Connect to the database
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    # Fetch readings to compute each account's bill
    pendingBalanceCalculate = cursor.execute("select accountNumber, previousReading, currentReading from readings").fetchall()

    # Try reading the kWh rate from the config JSON file
    # now instead of kWh rate being hardcoded into the source code
    # it can now be accessed in the json file, this allows kWh rate
    # to be easily changed instead of actually changing the code itself
    try:
        with open('configs.json', 'r') as file:
            data = json.load(file)
            kWhRateFetch = data['kWhRate'] # Fetch the kWh rate

    except FileNotFoundError:
        print("Error: JSON File not found!")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format!")
    except Exception as e:
        print(f"An unexpected error occured: {e}")

    # Loop through each reading and compute the total payment
    for reading in pendingBalanceCalculate:
        # kWhRateFetch is from the configs.json file
        totalPaymentWithoutVat = kWhRateFetch * (reading[2] - reading[1]) # Compute bill = rate * (currentReading - previousReading)
        addVat = totalPaymentWithoutVat * 0.12 # Add 12% VAT
        totalPaymentWithVat = addVat + totalPaymentWithoutVat

        # pendingBalance gets appended, while paymentThisBillingPeriod gets overwritten 
        cursor.execute("update accounts set pendingBalance = pendingBalance + ?, paymentThisBillingPeriod = ? where accountNumber = ?", (totalPaymentWithVat, totalPaymentWithVat, reading[0]))

    # Fetch all accounts that are currently marked as "paid"
    accountFetch3 = cursor.execute("select accountNumber from accounts where paymentStatus = 'paid'").fetchall()

    # Set their payment status to "unpaid" and notifications to not viewed
    for row3 in accountFetch3:

        cursor.execute("update accounts set paymentStatus = 'unpaid' where accountNumber = ?", (row3[0],))
        cursor.execute("update notifications set viewed = 'false' where accountNumber = ?", (row3[0],))

    # Save changes to the database
    connection.commit()
schedule.every().day.at("00:00").do(job1) # Schedule job1 to run every day at midnight
schedule.every().day.at("00:01").do(job2) # Schedule job2 to run every day at 12:01 AM

while True: # Keep checking for scheduled tasks
    schedule.run_pending() # Run due scheduled tasks
    time.sleep(1) # Sleep for 1 second before checking again
