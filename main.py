from databaseTables import Database
from loginWindow import loginWindow
from subProcess import subProcess

if __name__ == "__main__":
    Database()
    subProcess("kwh.py")
    subProcess("billScript.py")
    subProcess("ifUserPaid.py")
    loginWindow()
