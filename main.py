from databaseTables import Database
from loginWindow import loginWindow
from subProcess import subProcess

# (Automated) Electric Billing System
# IT121 Computer Programming Finals Performance Innovative Task
# BSIT-1R1

# ROA, Alexus Enzo
# MORENO, Dennis
# NAZARENO, Charles Archie
# YU, Mark Lester
# GUMATAY, Nick Adrienne

if __name__ == "__main__":
    Database()                      # Runs the database and create necessary tables if they don't exist
    subProcess("kwh.py")            # Calculates kilowatt-hour consumption 
    subProcess("billScript.py")     # Computes and stores billing amounts
    subProcess("ifUserPaid.py")     # Checks and updates user payment status
    loginWindow()                   # Launch the login window as the starting point of the application
