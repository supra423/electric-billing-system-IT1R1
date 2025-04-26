import sqlite3


class Database:
    def __init__(self):

        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()

        self.cursor.executescript(

            """
            CREATE TABLE IF NOT EXISTS accounts 
            (

                name TEXT NOT NULL,
                account_number TEXT NOT NULL,
                password TEXT NOT NULL,
                address TEXT NOT NULL,
                kWh INTEGER NOT NULL,
                balance INTEGER NOT NULL
            
            );
            """
        )
        self.connection.commit()
