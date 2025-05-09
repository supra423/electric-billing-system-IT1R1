import sqlite3
import tkinter as tk
from tkinter import messagebox

class createAccount():  

    def __init__(self):

        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()
        

        self.createAccountWindow = tk.Tk()
        self.createAccountWindow.title("Create an account")
        self.createAccountWindow.geometry("450x500")
        self.createAccountWindow.resizable(False, False)
        self.createAccountWindow.configure(bg = "#bbbbbb")

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
                bg = "#cccccc").pack(side="right", padx=20)

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
            
            accountFetch = self.cursor.execute("select accountNumber from accounts where accountNumber = ?",
                                                    (newAccountNumber,)).fetchone()
            if accountFetch:
                messagebox.showinfo('Error!', 'That account already exists!')
                return
            
            if len(newAccountNumber) != 16:
                messagebox.showinfo('Error!', 'Account number must be 16-digits')
                return
            
            if not newAccountNumber.isdigit():
                messagebox.showinfo('Error!', 'Account number must all be digits!')
                return

            installationFee = float(installationFee)

            if installationFee < 5000:
                messagebox.showinfo("Invalid payment!", "Please pay the proper amount!")
                return
            elif installationFee > 5000:
                messagebox.showinfo("Change", f"Here is your change: {installationFee - 5000:.2f}")

            self.cursor.execute("insert into accounts(name, accountNumber, password, address) values(?, ?, ?, ?)", 
                                (newName, newAccountNumber, newPassword, newHomeAddress))

            self.cursor.execute("insert into notifications(accountNumber) values(?)", (newAccountNumber,))

            self.cursor.execute("insert into readings(accountNumber) values(?)", (newAccountNumber,))

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
