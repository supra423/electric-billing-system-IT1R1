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

        # Connect to the SQLite database file (creates it if it doesn't exist)
        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()

        # Execute multiple SQL commands to create tables if they do not already exist
        self.cursor.executescript(

            """
            CREATE TABLE IF NOT EXISTS accounts 
            (
                name TEXT NOT NULL,                                     -- Full name of the account holder
                accountNumber TEXT NOT NULL,                            -- Unique 16-digit account number
                password TEXT NOT NULL,                                 -- Account password
                address TEXT NOT NULL,                                  -- User's home address
                kWh INTEGER DEFAULT 0,                                  -- Total kilowatt-hours consumed (default 0)
                paymentStatus TEXT DEFAULT 'paid',                      -- Current payment status (default 'paid')
                accountStatus TEXT DEFAULT 'active',                    -- Account status (active/inactive)
                paidLastMonth TEXT DEFAULT 'true',                      -- Whether last month's bill was paid
                paymentLastBillingPeriod INTEGER DEFAULT 0,             -- Amount paid in last billing period
                paymentThisBillingPeriod INTEGER DEFAULT 0,             -- Amount paid in current billing period
                pendingBalance INTEGER DEFAULT 0                        -- Any pending balance owed
            );

            CREATE TABLE IF NOT EXISTS notifications
            (
                accountNumber TEXT NOT NULL,                            -- Links notification to an account
                viewed TEXT DEFAULT 'true'                              -- Ambot lang
            );

            CREATE TABLE IF NOT EXISTS history 
            (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,          -- Unique ID for each transaction record
                accountNumber TEXT NOT NULL,                            -- Account associated with the payment
                amountPaid INTEGER NOT NULL,                            -- Amount paid in the transaction
                timestamp TEXT NOT NULL                                 -- Date/time when payment was made
            );

            CREATE TABLE IF NOT EXISTS readings
            (
                accountNumber TEXT NOT NULL,                            -- Account linked to these meter readings
                previousReading INTEGER DEFAULT 0,                      -- Previous meter reading value
                currentReading INTEGER DEFAULT 0,                       -- Current meter reading value
                previousReadingDate TEXT DEFAULT 'N/A',                 -- Date of previous reading
                currentReadingDate TEXT DEFAULT 'N/A',                  -- Date of current reading
                dueDate TEXT DEFAULT 'N/A',                             -- Due date for payment
                disconnectionDate TEXT DEFAULT 'N/A'                    -- Date when service will be disconnected if unpaid
            );
            """
        )
        self.connection.commit()
