import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from helpWindow import helpWindow
from windowMain import mainMenu

class loginWindow():
    def __init__(self):

        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()

        self.loginWindow = tk.Tk()
        self.loginWindow.title("Login")
        self.loginWindow.geometry("350x400")
        self.loginWindow.resizable(False, False)
        self.loginWindow.configure(bg = "#bbbbbb")
        self.loginWindow.rowconfigure(2, weight = 1)
        self.loginWindow.columnconfigure(0, weight = 1)

        self.widgetFrame = tk.Frame(self.loginWindow, bg = "#bbbbbb")

        self.widgetFrame.rowconfigure(0, weight = 1)
        self.widgetFrame.columnconfigure(0, weight = 1)

        self.widgetFrame.grid(row = 0, column = 0, pady = 10, sticky = "nsew")

        tk.Label(self.widgetFrame,
                text = "Welcome!",
                font = ("Arial", 30),
                bg = "#bbbbbb",
                anchor = "center").pack(fill = "x", pady = 10)

        self.accountNumberEntry = self.labelAndEntry(self.widgetFrame, True, "Enter account number:", 20, 5, 5)
        self.passwordEntry = self.labelAndEntry(self.widgetFrame, False, "Enter Password:", 20, 5, 5)

        self.loginWindow.bind('<Return>', lambda event: self.login())
        self.loginWindow.bind('<Escape>', lambda event: self.loginWindow.destroy())

        self.buttonFrame = tk.Frame(self.loginWindow, bg = "#bbbbbb")

        self.buttonFrame.rowconfigure(0, weight = 1)
        self.buttonFrame.columnconfigure(1, weight = 1)

        self.buttonFrame.grid(row = 1, column = 0, pady = 5)

        tk.Button(self.buttonFrame,
                text = "Create \nnew account?",
                width = 15,
                height = 2,
                command = self.createAccountMenu,
                bg = "#cccccc").grid(padx = 20, row = 0, column = 0, sticky = "ew")

        tk.Button(self.buttonFrame,
                text = "Login",
                width = 15,
                height = 2,
                command = self.login,
                bg = "#cccccc").grid(padx = 20, row = 0, column = 1, sticky = "ew")

        self.helpFrame = tk.Frame(self.loginWindow, bg = "#bbbbbb")

        self.helpFrame.rowconfigure(0, weight = 1)
        self.helpFrame.columnconfigure(1, weight = 1)

        self.helpFrame.grid(row = 2, column = 0, pady = 5)

        self.helpButton = tk.Button(self.helpFrame,
                                    text = "Help?",
                                    width = 15,
                                    height = 2,
                                    bg = "#cccccc",
                                    command = self.helpButtonCommand)
        self.helpButton.grid(row = 0, column = 0, padx = 60, pady = 10)

        self.loginWindow.mainloop()

    def createAccountMenu(self):
        from createAccount import createAccount
        # lazy import I used to apply inheritance just to
        # open the create account window but I decided to just
        # use lazy import instead
        createAccount()

    def helpButtonCommand(self):
        helpWindow("loginWindow")

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

    def labelAndEntry(self, whichWindow, showEntry, labelText, fontSize, labelPady, entryPady):
        '''
        just a helper function to reduce the amount of lines
        input the text of the label and then the size of the text
        '''

        tk.Label(whichWindow,
                 text = labelText,
                 font = ("Arial", fontSize),
                 bg = "#bbbbbb").pack(pady = labelPady)

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

        newEntry.pack(pady = entryPady)

        return newEntry
