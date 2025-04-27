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
                accountNumber TEXT NOT NULL,
                password TEXT NOT NULL,
                address TEXT NOT NULL,
                kWh INTEGER NOT NULL DEFAULT 0,
                balance INTEGER NOT NULL DEFAULT 0
            
            );
            """
        )
        self.connection.commit()
