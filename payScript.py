import sqlite3

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

    connection.commit()
