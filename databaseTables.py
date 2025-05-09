import sqlite3


class Database:
    """
    Class for the database tables
    1st table is the main table for the accounts

    2nd table is for the notifications when the user
    clicks on the notification bell icon, this basically acts
    as some sort of "flag"

    3rd table is for transaction history everytime
    a user pays their bill

    4th table is for the meter readings so that the
    total kWh consumed the entire month can be determined 
    """
    def __init__(self):

        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()

        self.cursor.executescript(

            """
            CREATE TABLE IF NOT EXISTS accounts 
            (
                name TEXT NOT NULL,
                accountNumber TEXT NOT NULL,
                password TEXT NOT NULL,
                address TEXT NOT NULL,
                kWh INTEGER DEFAULT 0,
                paymentStatus TEXT DEFAULT 'unpaid',
                paymentLastBillingPeriod INTEGER DEFAULT 0,
                paymentThisBillingPeriod INTEGER DEFAULT 0,
                pendingBalance INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS notifications
            (
                accountNumber TEXT NOT NULL,
                viewed TEXT DEFAULT 'true'
            );

            CREATE TABLE IF NOT EXISTS history 
            (
                accountNumber TEXT NOT NULL,
                amountPaid INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS readings
            (
                accountNumber TEXT NOT NULL,
                previousReading INTEGER DEFAULT 0,
                currentReading INTEGER DEFAULT 0,
                previousReadingDate TEXT DEFAULT 'N/A',
                currentReadingDate TEXT DEFAULT 'N/A',
                dueDate TEXT DEFAULT 'N/A'
            );
            """
        )
        self.connection.commit()
