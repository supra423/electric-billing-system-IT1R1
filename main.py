import tkinter as tk
from tkinter import messagebox

from databaseTables import Database
from windowMain import mainMenu


class createAccount(Database): # defined this class first so that 
                               # accountLogin class can inherit from this class
                               # this class also inherits the Database class to
                               # insert new accounts into the database
    def __init__(self):

        self.createAccountWindow = tk.Tk()
        self.createAccountWindow.title("Create an account")
        self.createAccountWindow.geometry("400x400")
        self.createAccountWindow.resizable(False, False)

        # new name
        self.newNameEntry = self.labelAndEntry(self.createAccountWindow, True, "Enter name:", 20)
        # new account number
        self.newAccountNumberEntry = self.labelAndEntry(self.createAccountWindow, True, "Enter new account number\n(Must be 16 digits long):", 20)
        # home address
        self.newHomeAddressEntry = self.labelAndEntry(self.createAccountWindow, True, "Enter home address:", 20)
        # new password 
        self.newPasswordEntry = self.labelAndEntry(self.createAccountWindow, False, "Enter new password:", 20)
        # confirm new password
        self.newPasswordConfirmEntry = self.labelAndEntry(self.createAccountWindow, False, "Confirm new password:", 20)


        tk.Button(self.createAccountWindow, 
                text = "Create \nnew account", 
                width = 15, 
                height = 2, 
                command = self.insertNewAccount).pack(side="right", padx=20)

        self.createAccountWindow.mainloop()

    def insertNewAccount(self):
        try:
            newName = self.newNameEntry.get()
            newAccountNumber = self.newAccountNumberEntry.get()
            newHomeAddress = self.newHomeAddressEntry.get()
            newPassword = self.newPasswordEntry.get()
            newPasswordConfirm = self.newPasswordConfirmEntry.get()

        except Exception:
            messagebox.showinfo("Error!", "Error, please try again!")        

    
    def labelAndEntry(self, whichWindow, showEntry, labelText, fontSize):
        '''
        just a helper function to reduce the amount of lines
        input the text of the label and then the size of the text
        '''

        tk.Label(whichWindow,
                 text = labelText, 
                 font = ("Arial", fontSize)).pack()
            
        if showEntry:    

            newEntry = tk.Entry(whichWindow, 
                                width = 20,
                                font = ("Arial", 12))
        else:
            
            newEntry = tk.Entry(whichWindow,
                                width = 20,
                                font = ("Arial", 12),
                                show = "*")
        newEntry.pack()
        return newEntry

class accountLogin(createAccount, Database): # inherit methods from Database class for logging in to accounts
                                             # and createAccount class to open a create account window
    def __init__(self):
        self.loginWindow = tk.Tk()
        self.loginWindow.title("Login")
        self.loginWindow.geometry("300x400")
        self.loginWindow.resizable(False, False)

        tk.Label(self.loginWindow, 
                text = "Welcome!", 
                width = 10, 
                height = 3, 
                font = ("Arial", 30)).pack()

        self.nameEntry = self.labelAndEntry(self.loginWindow, True, "Enter Name:", 20)

        self.accountNumberEntry = self.labelAndEntry(self.loginWindow, True, "Enter account number:", 20)
        
        self.passwordEntry = self.labelAndEntry(self.loginWindow, False, "Enter Password:", 20)

        tk.Button(self.loginWindow, 
                text = "Login", 
                width = 15, 
                height = 2, 
                command = self.login).pack(side="right", padx=20)

        tk.Button(self.loginWindow, 
                text = "Create \nnew account?", 
                width = 15, 
                height = 2, 
                command = self.createAccountMenu).pack(side="left", padx=20)

        self.loginWindow.mainloop()

    def createAccountMenu(self):
        window = createAccount()

    def login(self):
        try:
            name = self.nameEntry.get()
            accountNumber = self.accountNumberEntry.get()
            password = self.passwordEntry.get()

            if name == "admin" and password == "1234" and password == "1234":
                self.loginWindow.destroy()
                mainMenu()

        except Exception:
            messagebox.showinfo("Error!", "Error, please try again!")

if __name__ == "__main__":
    accountLogin()
    Database()
