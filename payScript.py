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

    cursor.execute("update readings set disconnectionDate = 'N/A' where accountNumber = ?", (userAccountNumber,))

    connection.commit()

    paymentStatusCheck = cursor.execute("select paymentLastBillingPeriod, paymentThisBillingPeriod, pendingBalance from accounts where accountNumber = ?", (userAccountNumber,)).fetchone()

    if paymentStatusCheck[0] == 0 and paymentStatusCheck[1] == 0 and paymentStatusCheck[2] == 0:
        cursor.execute("update accounts set paymentStatus = 'paid' where accountNumber = ?", (userAccountNumber,))
    
    connection.commit()
