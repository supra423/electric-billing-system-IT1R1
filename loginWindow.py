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

        welcomeFrame = tk.Frame(self.loginWindow, bg = "#bbbbbb")
        welcomeFrame.pack(fill = "x", pady = 10)

        tk.Label(welcomeFrame, 
                text = "Welcome!", 
                font = ("Arial", 30), 
                bg = "#bbbbbb", 
                anchor = "center").pack(fill = "x", pady = (40, 20))
            

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

            accountExists = self.cursor.execute("SELECT name, accountNumber, address, password FROM accounts WHERE accountNumber = ?", (accountNumber,)).fetchone()

            if not accountExists:
                messagebox.showinfo('Error!', 'That account does not exist!') ## ADDED
                return 

            if password != accountExists[3]: ## ADDED
                messagebox.showinfo('Error!', 'Incorrect password!') ## ADDED
                return
            
            self.loginWindow.destroy()
            mainMenu((accountExists))

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
