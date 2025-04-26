import tkinter as tk
from tkinter import messagebox

from databaseTables import Database
from windowMain import mainMenu


class createAccount: # defined this class first so that accountLogin class can inherit from this class

    def insertNewAccount(self):
       self.newName = self.newNameEntry.get()
       self.newAccountNumber = self.newAccountNumberEntry.get()
       self.newHomeAddress = self.newHomeAddressEntry.get()
       self.newPassword = self.newPasswordEntry.get()
       self.newPasswordConfirm = self.newPasswordConfirmEntry.get()

    def __init__(self):

        self.createAccountWindow = tk.Tk()
        self.createAccountWindow.title("Create an account")
        self.createAccountWindow.geometry("400x400")
        self.createAccountWindow.resizable(False, False)
        
        # new name
        tk.Label(self.createAccountWindow,
                 text = "Enter name:",
                 font = ("Arial", 20)).pack()
        
        self.newNameEntry = tk.Entry(self.createAccountWindow,
                                     width = 20,
                                     font = ("Arial", 12)).pack()
        # new accout number
        tk.Label(self.createAccountWindow,
                 text = "Enter new Account Number\n(Must be 16 digits long):",
                 font = ("Arial", 20)).pack()
        
        self.newAccountNumberEntry = tk.Entry(self.createAccountWindow,
                                     width = 20,
                                     font = ("Arial", 12)).pack()
        
        # home address
        tk.Label(self.createAccountWindow,
                 text = "Home address:",
                 font = ("Arial", 20)).pack()
        
        self.newHomeAddressEntry = tk.Entry(self.createAccountWindow,
                                     width = 20,
                                     font = ("Arial", 12)).pack()
       
        # new password
        tk.Label(self.createAccountWindow,
                 text = "Enter new password:",
                 font = ("Arial", 20)).pack()
        
        self.newPasswordEntry = tk.Entry(self.createAccountWindow,
                                     width = 20,
                                     font = ("Arial", 12),
                                     show = "*").pack()
        # confirm new password
        tk.Label(self.createAccountWindow,
                 text = "Confirm new password:",
                 font = ("Arial", 20)).pack()
        
        self.newPasswordConfirmEntry = tk.Entry(self.createAccountWindow,
                                     width = 20,
                                     font = ("Arial", 12),
                                     show = "*").pack()
        tk.Button(self.createAccountWindow, 
                text = "Create \nnew account", 
                width = 15, 
                height = 2, 
                command = self.insertNewAccount).pack(side="right", padx=20)

class accountLogin(Database, createAccount): # inherit methods from Database class and createAccount class
    def createAccountMenu(self):
        window = createAccount()

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

        tk.Label(self.loginWindow, 
                text = "Name", 
                width = 10, 
                height = 1, 
                font = ("Arial", 20)).pack()

        self.nameEntry = tk.Entry(self.loginWindow, 
                            width = 20, 
                            font = ("Arial", 12))
        self.nameEntry.pack()

        tk.Label(self.loginWindow,
                text = "Account Number",
                width = 15, 
                height = 1, 
                font = ("Arial", 20)).pack()
        self.accountEntry = tk.Entry(self.loginWindow, 
                                width = 20, 
                                font = ("Arial", 12))
        self.accountEntry.pack()

        tk.Label(self.loginWindow, 
                text = "Password", 
                width = 10, 
                height = 1, 
                font = ("Arial", 20)).pack()
        self.passwordEntry = tk.Entry(self.loginWindow, 
                                width = 20, 
                                font = ("Arial", 12), 
                                show = "*")
        self.passwordEntry.pack()

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
