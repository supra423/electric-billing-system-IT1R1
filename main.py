from databaseTables import Database
from loginWindow import accountLogin
from subProcess import subProcess

if __name__ == "__main__":
    Database()
    subProcess("kwh.py")
    subProcess("billScript.py")
    accountLogin()
