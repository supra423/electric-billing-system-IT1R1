from databaseTables import Database
from loginWindow import loginWindow
from subProcess import subProcess

# (Automated) Electric Billing System
# IT121 Computer Programming Finals Performance Innovative Task
# BSIT-1R1

# ROA, Alexus Enzo
# MORENO, Dennis
# Nazareno, Charles Archie
# Yu, Mark Lester
# Gumatay, Nick Adrienne

if __name__ == "__main__":
    Database()
    subProcess("kwh.py")
    subProcess("billScript.py")
    subProcess("ifUserPaid.py")
    loginWindow()
