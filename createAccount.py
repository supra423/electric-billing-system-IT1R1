import sqlite3
import tkinter as tk
from tkinter import messagebox
import json
from PIL import Image, ImageTk
from helpWindow import helpWindow

class createAccount():

    def __init__(self):
        # Connect to SQLite database file or create it if not exists
        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()

        # Setup the main window for account creation using Tkinter
        self.createAccountWindow = tk.Tk()
        self.createAccountWindow.title("Create an account")
        self.createAccountWindow.geometry("450x500")
        self.createAccountWindow.resizable(False, False) # Fix window size
        self.createAccountWindow.configure(bg = "#bbbbbb")

        self.createAccountWindow.columnconfigure(0, weight = 1)
        self.createAccountWindow.rowconfigure(1, weight = 1)

        # Load installation fee configuration from JSON file
        try:
            with open('configs.json', 'r') as file:
                data = json.load(file)
                self.installationFeeFetch = float(data['installationFee']) # Store fee as float

        except FileNotFoundError:
            print("Error: JSON File not found!")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format!")
        except Exception as e:
            print(f"An unexpected error occured: {e}")

        self.widgetFrame = tk.Frame(self.createAccountWindow, bg = "#bbbbbb")
        self.widgetFrame.grid(row = 0, column = 0, pady = 5, sticky = "ns")

        # new name
        self.newNameEntry = self.labelAndEntry(self.widgetFrame, True, "Enter name:", 20)
        # new account number
        self.newAccountNumberEntry = self.labelAndEntry(self.widgetFrame, True, "Enter new account number\n(Must be 16 digits long):", 20)
        # home address
        self.newHomeAddressEntry = self.labelAndEntry(self.widgetFrame, True, "Enter home address:", 20)
        # new password 
        self.newPasswordEntry = self.labelAndEntry(self.widgetFrame, False, "Enter new password:", 20)
        # confirm new password
        self.newPasswordConfirmEntry = self.labelAndEntry(self.widgetFrame, False, "Confirm new password:", 20)
        # initial payment for installation
        self.installationFee = self.labelAndEntry(self.widgetFrame, True, f"Installation fee\n(₱{self.installationFeeFetch:.2f}):", 20)

        # Bind keyboard keys: Enter to submit, Escape to close window
        self.createAccountWindow.bind('<Return>', lambda event: self.insertNewAccount())
        self.createAccountWindow.bind('<Escape>', lambda event: self.createAccountWindow.destroy())


        self.buttonFrame = tk.Frame(self.createAccountWindow, bg = "#bbbbbb")

        self.buttonFrame.rowconfigure(0, weight = 1)
        self.buttonFrame.columnconfigure(1, weight = 1)

        self.buttonFrame.grid(row = 1, column = 0, pady = 5)

        # Help button to open help window
        self.helpButton = tk.Button(self.buttonFrame,
                                    text = "Help?",
                                    width = 12,
                                    height = 2,
                                    bg = "#cccccc",
                                    command = self.helpButtonCommand)
        self.helpButton.grid(row = 0, column = 0, padx = 60, pady = 10)

        # Button to create a new account
        self.newAccountButton = tk.Button(self.buttonFrame, 
                text = "Create \nnew account", 
                width = 12, 
                height = 2, 
                command = self.insertNewAccount,
                bg = "#cccccc")

        self.newAccountButton.grid(row = 0, column = 1, padx = 60, pady = 10)

        # Start the GUI event loop
        self.createAccountWindow.mainloop()

    def insertNewAccount(self):
        try:
            # Get all user input, strip extra whitespace
            newName = self.newNameEntry.get().strip()
            newAccountNumber = self.newAccountNumberEntry.get().strip().replace(" ", "")
            newHomeAddress = self.newHomeAddressEntry.get().strip()
            newPassword = self.newPasswordEntry.get().strip()
            newPasswordConfirm = self.newPasswordConfirmEntry.get().strip()
            installationFee = self.installationFee.get().strip()


            # error message list that contains the type of empty string error and the error message that corresponds to it
            emptyEntryMessages = (
                    (newName, 'Please enter your name'),
                    (newAccountNumber, 'Please enter your account number!'),
                    (newHomeAddress, 'Please enter your home address!'),
                    (newPassword, 'Please enter your password'),
                    (newPasswordConfirm, 'Please confirm your password!'),
                    (installationFee, 'Please pay the installation fee!')
            )

            for errorTuple in emptyEntryMessages:
                if not errorTuple[0]:
                    messagebox.showinfo('Error!', errorTuple[1])
                    return # Stop function if any input is empty

            # Check that password and confirmation match
            if newPassword != newPasswordConfirm:
                messagebox.showinfo('Error!', 'Password confirmation is incorrect!')
                return

            # Check if the account number already exists in the database
            accountFetch = self.cursor.execute("select accountNumber from accounts where accountNumber = ?",
                                                    (newAccountNumber,)).fetchone()
            if accountFetch:
                messagebox.showinfo('Error!', 'That account already exists!')
                return
            
            # Validate account number length and numeric-only characters
            if len(newAccountNumber) != 16:
                messagebox.showinfo('Error!', 'Account number must be 16-digits')
                return
            if not newAccountNumber.isdigit():
                messagebox.showinfo('Error!', 'Account number must all be digits!')
                return

            installationFee = float(installationFee)

            # comparing the installation fee to the installation fee fetched from the configs.json file
            if installationFee < self.installationFeeFetch:
                messagebox.showinfo("Invalid payment!", "Please pay the proper amount!")
                return
            # Inform user if they overpaid and provide change
            elif installationFee > self.installationFeeFetch:
                messagebox.showinfo("Change", f"Here is your change: {installationFee - self.installationFeeFetch:.2f}")

            # Insert new account data into database tables
            self.cursor.execute("insert into accounts(name, accountNumber, password, address) values(?, ?, ?, ?)", 
                                (newName, newAccountNumber, newPassword, newHomeAddress))

            #Create notifications and readings with the new account number
            self.cursor.execute("insert into notifications(accountNumber) values(?)", (newAccountNumber,))

            self.cursor.execute("insert into readings(accountNumber) values(?)", (newAccountNumber,))

            # Save changes to the database
            self.connection.commit()

            # Notify user of successful registration and close the window
            messagebox.showinfo("Thank you!", "Thank you for joining EPALCO!")
            self.createAccountWindow.destroy()

        except Exception as e:
            messagebox.showinfo("Error!", "Error, please try again!\n")        
            print(e)

    def helpButtonCommand(self):
        # Open the help window related to account creation
        helpWindow("createAccount")

    def labelAndEntry(self, whichWindow, showEntry, labelText, fontSize):
        '''
        just a helper function to reduce the amount of lines
        input the text of the label and then the size of the text
        '''

        tk.Label(whichWindow,
                 text = labelText, 
                 font = ("Arial", fontSize),
                 bg = "#bbbbbb").grid(column = 0)

        if showEntry:

            newEntry = tk.Entry(whichWindow, 
                                width = 20,
                                font = ("Arial", 12),
                                bg = "#eeeeee")
        else:

            newEntry = tk.Entry(whichWindow,
                                width = 20,
                                font = ("Arial", 12),
                                show = "*", # hides input for passwords
                                bg = "#eeeeee")

        newEntry.grid(column = 0)
        return newEntry

