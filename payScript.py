import sqlite3

"""
These functions are basically helper functions that are called when somebody makes
a successful payment. 

1st function basically pays every balance, this sets the paymentLastBillingPeriod, 
paymentThisBillingPeriod, and the pendingBalance to 0. the paymentStatus is set to = 'paid'
the account status is set to 'active' and the paidLastMonth is set to 'true'

the 2nd function just pays the paymentLastBillingPeriod setting it to 0 and then minuses the pendingBalance to
paymentLastBillingPeriod (pendingBalance = pendingBalance - paymentLastBillingPeriod)

now everytime this function gets called, it also checks if a particular user has:
paymentThisBillingPeriod, paymentLastBillingPeriod, pendingBalance = 0

if so, then just automatically update their paymentStatus to paid
"""

def payAll(userAccountNumber):
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    cursor.execute("""
        update accounts set 
            paymentStatus = 'paid', 
            accountStatus = 'active', 
            paidLastMonth = 'true', 
            paymentLastBillingPeriod = 0, 
            paymentThisBillingPeriod = 0,
            pendingBalance = 0
        WHERE accountNumber = ?
    """, (userAccountNumber,))

    # if user has a disconnectionDate, update it to N/A so that they don't get terminated
    cursor.execute("update readings set disconnectionDate = 'N/A' where accountNumber = ?", (userAccountNumber,))

    connection.commit()

def payOnlyLastMonth(userAccountNumber):
    connection = sqlite3.connect('database.s3db')
    cursor = connection.cursor()

    paymentLastBillingPeriodFetch = cursor.execute("select paymentLastBillingPeriod from accounts where accountNumber = ?", (userAccountNumber,)).fetchone()

    cursor.execute("""
        update accounts set
            paidLastMonth = 'true',
            accountStatus = 'active',
            pendingBalance = pendingBalance - ?,
            paymentLastBillingPeriod = 0
        where accountNumber = ?
    """, (paymentLastBillingPeriodFetch[0], userAccountNumber))

    # if user has a disconnectionDate, update it to N/A so that they don't get terminated
    cursor.execute("update readings set disconnectionDate = 'N/A' where accountNumber = ?", (userAccountNumber,))

    connection.commit()

    paymentStatusCheck = cursor.execute("select paymentLastBillingPeriod, paymentThisBillingPeriod, pendingBalance from accounts where accountNumber = ?", (userAccountNumber,)).fetchone()

    if paymentStatusCheck[0] == 0 and paymentStatusCheck[1] == 0 and paymentStatusCheck[2] == 0:
        cursor.execute("update accounts set paymentStatus = 'paid' where accountNumber = ?", (userAccountNumber,))
    
    connection.commit()
