import sqlite3
import tkinter as tk
from tkinter import messagebox

from windowMain import mainMenu


class createAccount():  

    def __init__(self):

        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()
        

        self.createAccountWindow = tk.Tk()
        self.createAccountWindow.title("Create an account")
        self.createAccountWindow.geometry("450x500")
        self.createAccountWindow.resizable(False, False)
        self.createAccountWindow.configure(bg = "#aaaaaa")

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
        # initial payment for installation
        self.installationFee = self.labelAndEntry(self.createAccountWindow, True, "Installation fee\n(Php. 5,000.00):", 20)

        tk.Button(self.createAccountWindow, 
                text = "Create \nnew account", 
                width = 15, 
                height = 2, 
                command = self.insertNewAccount,
                bg = "#c6c6c6").pack(side="right", padx=20)

        self.createAccountWindow.mainloop()

    def insertNewAccount(self):
        try:
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
                    return 
                
            if newPassword != newPasswordConfirm:
                messagebox.showinfo('Error!', 'Password confirmation is incorrect!')
                return
            
            installationFee = float(installationFee)

            if installationFee < 5000:
                messagebox.showinfo("Invalid payment!", "Please pay the proper amount!")
                return
            elif installationFee > 5000:
                messagebox.showinfo("Change", f"Here is your change: {installationFee - 5000:.2f}")
            else:
                pass

            accountFetch = self.cursor.execute("select accountNumber from accounts where accountNumber = ?",
                                                    (newAccountNumber,)).fetchone()
            if accountFetch:
                messagebox.showinfo('Error!', 'That account already exists!')
                return
            
            if len(newAccountNumber) != 16:
                messagebox.showinfo('Error!', 'Account number must be 16-digits')
                return

            self.cursor.execute("insert into accounts(name, accountNumber, password, address) values(?, ?, ?, ?)", 
                                (newName, newAccountNumber, newPassword, newHomeAddress))
            self.connection.commit()
            messagebox.showinfo("Thank you!", "Thank you for joining EPALCO!")
            self.createAccountWindow.destroy()

        except Exception as e:
            messagebox.showinfo("Error!", "Error, please try again!\n")        
            print(e)            
    def labelAndEntry(self, whichWindow, showEntry, labelText, fontSize):
        '''
        just a helper function to reduce the amount of lines
        input the text of the label and then the size of the text
        '''

        tk.Label(whichWindow,
                 text = labelText, 
                 font = ("Arial", fontSize),
                 bg = "#aaaaaa").pack()
            
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

class accountLogin(createAccount): # inherit from createAccount class to open a create 
                                   # account window and borrow the labelAndEntry function
    def __init__(self):

        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()

        self.loginWindow = tk.Tk()
        self.loginWindow.title("Login")
        self.loginWindow.geometry("300x400")
        self.loginWindow.resizable(False, False)
        self.loginWindow.configure(bg = "#aaaaaa")

        tk.Label(self.loginWindow, 
                text = "Welcome!", 
                width = 10, 
                height = 3, 
                font = ("Arial", 30),
                 bg = "#aaaaaa").pack()

        self.accountNumberEntry = self.labelAndEntry(self.loginWindow, True, "Enter account number:", 20)
        
        self.passwordEntry = self.labelAndEntry(self.loginWindow, False, "Enter Password:", 20)

        tk.Button(self.loginWindow, 
                text = "Login", 
                width = 15, 
                height = 2, 
                command = self.login,
                bg = "#c6c6c6").pack(side="right", padx=20)

        tk.Button(self.loginWindow, 
                text = "Create \nnew account?", 
                width = 15, 
                height = 2, 
                command = self.createAccountMenu,
                bg = "#c6c6c6").pack(side="left", padx=20)

        self.loginWindow.mainloop()

    def createAccountMenu(self):
        window = createAccount()

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

            accountFetch = self.cursor.execute("select accountNumber, password from accounts where accountNumber = ? and password = ?",
                                               (accountNumber, password)).fetchone()

            if accountFetch:
                self.loginWindow.destroy()
                mainMenu()
            else:
                messagebox.showinfo('Error!', 'That account does not exist!')

        except Exception as e:
            messagebox.showinfo("Error!", "Error, please try again!")
            print(e)
