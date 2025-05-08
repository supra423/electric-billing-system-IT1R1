import sqlite3
import tkinter as tk
from tkinter import messagebox

from windowMain import mainMenu

class loginWindow():
    def __init__(self):

        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()

        self.loginWindow = tk.Tk()
        self.loginWindow.title("Login")
        self.loginWindow.geometry("300x400")
        self.loginWindow.resizable(False, False)
        self.loginWindow.configure(bg = "#bbbbbb")

        tk.Label(self.loginWindow, 
                text = "Welcome!", 
                width = 10, 
                height = 3, 
                font = ("Arial", 30),
                bg = "#bbbbbb").pack()

        self.accountNumberEntry = self.labelAndEntry(self.loginWindow, True, "Enter account number:", 20)
        
        self.passwordEntry = self.labelAndEntry(self.loginWindow, False, "Enter Password:", 20)

        tk.Button(self.loginWindow, 
                text = "Login", 
                width = 15, 
                height = 2, 
                command = self.login,
                bg = "#cccccc").pack(side="right", padx=20)

        tk.Button(self.loginWindow, 
                text = "Create \nnew account?", 
                width = 15, 
                height = 2, 
                command = self.createAccountMenu,
                bg = "#cccccc").pack(side="left", padx=20)

        self.loginWindow.mainloop()

    def createAccountMenu(self):
        from createAccount import createAccount
        # lazy import I used to apply inheritance just to
        # open the create account window but I decided to just
        # use lazy import instead
        createAccount()

    def login(self):
        try:
            accountNumber = self.accountNumberEntry.get().strip().replace(" ", "")
            password = self.passwordEntry.get().strip()

            errorMessages = (
                (accountNumber, 'Please enter your account number!'),
                (password, 'Please enter your password!')
            )

            for errorTuple in errorMessages:
                if errorTuple[0] == '':
                    messagebox.showinfo('Error!', errorTuple[1])
                    return

                accountFetch = self.cursor.execute("select name, accountNumber, address from accounts where accountNumber = ? and password = ?",
                                               (accountNumber, password)).fetchone()

            if accountFetch:
                self.loginWindow.destroy()
                mainMenu(accountFetch)
            else:
                messagebox.showinfo('Error!', 'That account does not exist!')

        except Exception as e:
            messagebox.showinfo("Error!", "Error, please try again!")
            print(e)

    def labelAndEntry(self, whichWindow, showEntry, labelText, fontSize):
        '''
        just a helper function to reduce the amount of lines
        input the text of the label and then the size of the text
        '''

        tk.Label(whichWindow,
                 text = labelText, 
                 font = ("Arial", fontSize),
                 bg = "#bbbbbb").pack()
            
        if showEntry:    

            newEntry = tk.Entry(whichWindow, 
                                width = 20,
                                font = ("Arial", 12),
                                bg = "#eeeeee")
        else:
            
            newEntry = tk.Entry(whichWindow,
                                width = 20,
                                font = ("Arial", 12),
                                show = "*",
                                bg = "#eeeeee")

        newEntry.pack()
        return newEntry
