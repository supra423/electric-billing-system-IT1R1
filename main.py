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
        self.labelAndEntryCreateAccount("Enter name:", 20)
        # new account number
        self.labelAndEntryCreateAccount("Enter new account number\n(Must be 16 digits long):", 12)
        # home address
        self.labelAndEntryCreateAccount("Enter home address:", 20)
        # new password 
        self.labelAndEntryCreateAccount("Enter new password:", 20)
        # confirm new password
        self.labelAndEntryCreateAccount("Confirm new password:", 20)

        tk.Button(self.createAccountWindow, 
                text = "Create \nnew account", 
                width = 15, 
                height = 2, 
                command = self.insertNewAccount).pack(side="right", padx=20)


    def insertNewAccount(self):
        try:
            newName = self.newNameEntry.get()
            newAccountNumber = self.newAccountNumberEntry.get()
            newHomeAddress = self.newHomeAddressEntry.get()
            newPassword = self.newPasswordEntry.get()
            newPasswordConfirm = self.newPasswordConfirmEntry.get()
            
            if newPassword == newPasswordConfirm: 
                self.cursor.execute("insert into accounts(name, accountNumber, address, password) ") 


        except Exception:
            messagebox.showinfo("Error!", "Please don't leave any entries blank!")        

    
    def labelAndEntryCreateAccount(self, labelText, fontSize):
        '''
        just a helper function to reduce the amount of lines
        input the text of the label and then the size of the text
        '''
        tk.Label(self.createAccountWindow,
                 text = labelText,
                 font = ("Arial", fontSize)).pack()
        
        self.newNameEntry = tk.Entry(self.createAccountWindow,
                                     width = 20,
                                     font = ("Arial", 12)).pack()



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

        self.labelAndEntryAccountLogin("Enter Name:", 20)

        self.labelAndEntryAccountLogin("Enter account number:", 20)
        
        self.labelAndEntryAccountLogin("Enter Password:", 20)

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

    def labelAndEntryAccountLogin(self, labelText, fontSize):
        '''
        Another helper label and entry helper function but this time this is
        for the accountLogin class
        '''
        tk.Label(self.loginWindow, 
                text = labelText, 
                width = 17, 
                height = 1, 
                font = ("Arial", fontSize)).pack()

        self.nameEntry = tk.Entry(self.loginWindow, 
                            width = 20, 
                            font = ("Arial", 12))
        self.nameEntry.pack()

       

    def createAccountMenu(self):
        window = createAccount()

    def login(self):
        name = self.nameEntry.get()
        accountNumber = self.accountEntry.get()
        password = self.passwordEntry.get()

        if name == "admin" and password == "1234" and password == "1234":
            self.loginWindow.destroy()
            mainMenu()

if __name__ == "__main__":
    accountLogin()
    Database()
