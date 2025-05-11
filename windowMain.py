import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from payScript import payAll, payOnlyLastMonth
class mainMenu():

    def __init__(self, user):
        
        # user is basically a tuple that came from the accountFetch tuple in the loginWindow.py in the login() function
        # user[0] is the name, user[1] is the account number, user[2] is the address
        # this is important so that the program can identify which user is using the main window!
        self.username = user[0]
        self.accountNumber = user[1]
        self.address = user[2]

        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()

        self.mainWindow = tk.Tk()
        self.mainWindow.title("Main Menu")
        self.mainWindow.minsize(1000, 700)
        self.mainWindow.configure(bg = "#bbbbbb")

        # Configure the grid layout of the main window
        self.mainWindow.rowconfigure(0, weight=1)
        self.mainWindow.columnconfigure(1, weight=1)

        # Sidebar (column 0)
        self.sideBar = tk.Frame(self.mainWindow, bg = '#2c3e50', width = 200)
        self.sideBar.grid(row = 0, column = 0, sticky = "ns")

        # Content frame (column 1)
        self.contentFrame = tk.Frame(self.mainWindow, bg = "#bbbbbb")
        self.contentFrame.grid(row = 0, column = 1, sticky = "nsew")

        #  buttons
        tk.Button(self.sideBar,
                  text = "E P A L C O",
                  width = 10,
                  height = 1,
                  bg = "#2c3e50",
                  activebackground = "#2c3e50",
                  bd = 0,
                  fg = "#ffffff",
                  font = ("Arial", 16, "bold"),
                  command = self.mainPage).pack(pady = 10)

        self.mainButtons("Generate Bill", self.generateBill)
        self.mainButtons("Pay", self.pay)
        self.mainButtons("View transaction history", self.viewTransactionHistory)
        self.mainButtons("Logout", self.logout)

        self.mainPage() 

        self.mainWindow.mainloop()

    def mainButtons(self, buttonText, buttonCommand):
        tk.Button(self.sideBar,
                  text = buttonText,
                  width = 20,
                  height = 2,
                  activebackground = "#7baee0",
                  command = buttonCommand,
                  anchor = "w",
                  padx = 10,
                  bg = "#3f5a75",
                  fg = "#ffffff",
                  font = ("Arial", 16)).pack(pady = 10, fill = "x")

    def mainPage(self):
        self.clearContent()

        accountStatusCheck = self.cursor.execute("select accountStatus, pendingBalance from accounts where accountNumber = ?", (self.accountNumber,)).fetchone()
        kwhRead = self.cursor.execute("select kWh from accounts where accountNumber = ?", (self.accountNumber,)).fetchone()

        content = tk.Frame(self.contentFrame, bg = "#bbbbbb")
        content.grid(row = 1, column = 0, columnspan = 2, sticky = "nw", padx = 20, pady = 20)


        tk.Label(content,
                text = "Welcome!",
                 font = ("Arial", 40),
                 bg = "#bbbbbb").grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")

        tk.Label(content,
                 text = self.username,
                 font = ("Arial", 40),
                 bg = "#bbbbbb").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")

        tk.Label(content,
                 text = f"Electricity meter: {kwhRead[0]} kWh",
                 font = ("Arial", 30),
                 bg = "#bbbbbb").grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "w")

        if accountStatusCheck[0] == 'terminated':
            tk.Label(content,
                     text = "Your account has been terminated!",
                     font = ("Arial", 20),
                     bg = "#bbbbbb").grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "w")
            tk.Label(content,
                     text = f"Please pay the total balance: ₱{accountStatusCheck[1]:.2f}",
                     font = ("Arial", 20),
                     bg = "#bbbbbb").grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "w")

        #Please pay the total balance!
        self.bellIconSwitch()
    def generateBill(self):
        self.clearContent()
        # readings = (previousReading, currentReading, previousReadingDate, currentReadingDate)
        readings = self.cursor.execute("select previousReading, currentReading, previousReadingDate, currentReadingDate, dueDate from readings where accountNumber = ?", (self.accountNumber,)).fetchone()

        balanceFetch = self.cursor.execute("select paymentLastBillingPeriod, paymentThisBillingPeriod, pendingBalance, paymentStatus from accounts where accountNumber = ?", (self.accountNumber,)).fetchone()

        if balanceFetch[3] == 'unpaid' and balanceFetch[2]:
            totalKwhUsage = readings[1] - readings[0]

            totalPaymentWithoutVat = totalKwhUsage * 10
            addVat = totalPaymentWithoutVat * 0.12

            billFrame = tk.Frame(self.contentFrame, bg = "#ffffff", bd = 2, relief = "solid")
            billFrame.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")
            
            billTitle = tk.Label(billFrame,
                    text = " --- E P A L C O ---",
                    font = ("Arial", 20, 'italic'),
                    bg = "#ffffff")

            billTitle.pack(pady = 20)

            textFont = ("Arial", 14)

            billBody = tk.Text(billFrame, height = 17, width = 50, font = textFont)
            billBody.pack()

            billBody.insert('1.0', f"Name: {self.username}\n")
            billBody.insert('2.0', f"Address: {self.address}\n\n")
            billBody.insert('4.0', f"Billing period: {readings[2]} - {readings[3]}\n")
            billBody.insert('5.0', f"Previous reading - current reading (kWh): {readings[0]} - {readings[1]}\n")
            billBody.insert('6.0', f"Total kWh usage: {totalKwhUsage}\n\n")
            billBody.insert('8.0', f"PAY BEFORE: {readings[4]}\n")
            billBody.insert('9.0', f"Rate: ₱10/kWh\n")
            billBody.insert('10.0', f"Value-added Tax (VAT): 12%\n")
            billBody.insert('11.0', f"Total payment without VAT: ₱{totalPaymentWithoutVat:.2f}\n")
            billBody.insert('12.0', f"Added VAT: ₱{addVat:.2f}\n\n")
            billBody.insert('14.0', f"Total Payment this billing period: ₱{balanceFetch[1]:.2f}\n")
            billBody.insert('15.0', f"Unpaid balance last billing period (Ignore if ₱0.00): ₱{balanceFetch[0]:.2f}\n\n")
            billBody.insert('17.0', f"TOTAL PENDING BALANCE: ₱{balanceFetch[2]:.2f}\n")

            billBody.config(state = 'disabled')
        else:
            messagebox.showinfo("Notification!", "No bill is currently available!")
        self.bellIconSwitch()

    def pay(self):

        self.balance = self.cursor.execute("select pendingBalance, paymentLastBillingPeriod from accounts where accountNumber = ?", (self.accountNumber,)).fetchone()

        self.clearContent()

        self.LabelHelperFunction(tk.Label, "Pay Page", 24, "#bbbbbb", 0, False)
        self.LabelHelperFunction(tk.Label, "You have two options when paying:", 20, "#bbbbbb", 1, False)
        self.LabelHelperFunction(tk.Label, f"Pay all pending balance: ₱{self.balance[0]:.2f}", 20, "#bbbbbb", 2, False)

        self.LabelHelperFunction(tk.Button, "Pay all pending balance", 14, "#ababab", 3, True, lambda: self.buttonPayAllFunction("Pay All"))

        self.LabelHelperFunction(tk.Label, f"Pay only last month's bill (Ignore if ₱0.00): ₱{self.balance[1]:.2f}", 20, "#bbbbbb", 4, False)

        self.LabelHelperFunction(tk.Button, "Pay only last month's bill", 14, "#ababab", 5, True, lambda: self.buttonPayOnlyFunction("Pay Only Last Month"))

        self.bellIconSwitch()

    def LabelHelperFunction(self, labelOrButton, labelText, fontSize, bgColor, whichRow, buttonCommandBool, buttonPay = None):
        """
        helper function just to reduce some lines :)
        """

        if buttonCommandBool == False:
            labelOrButton(self.contentFrame,
                    text = labelText,
                    font = ("Arial", fontSize),
                    bg = bgColor).grid(row = whichRow, column = 0, padx = 5, pady = 5, sticky = "w")
        else:
            labelOrButton(self.contentFrame,
                    text = labelText,
                    font = ("Arial", fontSize),
                    bg = bgColor,
                    command = buttonPay).grid(row = whichRow, column = 0, padx = 5, pady = 5, sticky = "w")
    
    ### Payment window
    def buttonPayAllFunction(self, choice):
        self.payWindowWidgets(choice, payAll)

    def buttonPayOnlyFunction(self, choice):
        self.payWindowWidgets(choice, payOnlyLastMonth)

    def payWindowWidgets(self, choice, chosenFunction):
        self.payWindow = tk.Toplevel()
        self.payWindow.title(f"{choice}")
        self.payWindow.geometry("400x300")
        self.payWindow.resizable(False, False)
        self.payWindow.configure(bg = "#bbbbbb")

        for i in range(3):
            self.payWindow.columnconfigure(i, weight = 1)
            self.payWindow.rowconfigure(i, weight = 1)

        tk.Label(self.payWindow,
                 text = "Please enter the\nproper amount:",
                 font = ("Arial", 20),
                 bg = "#bbbbbb").grid(row = 0, column = 1)
        tk.Label(self.payWindow,
                 text = "₱",
                 font = ("Arial", 16),
                 bg = "#bbbbbb").grid(row = 1, column = 0, pady = 10, sticky = "e")

        self.paymentEntry = tk.Entry(self.payWindow, font = ('Arial', 16))
        self.paymentEntry.grid(row = 1, column = 1, pady = 10)

        tk.Button(self.payWindow,
                  text = "PAY",
                  font = ("Arial", 14),
                  bg = "#ababab",
                  command = lambda: self.paymentEntryGet(chosenFunction)).grid(row = 2, column = 2, pady = 10, sticky = "w")

    def paymentEntryGet(self, chosenFunction):
        paymentEntered = self.paymentEntry.get().strip()
        
        if not paymentEntered:
            messagebox.showinfo("Error!", "You haven't enterred a payment yet!")
            return

        paymentFetch = self.cursor.execute("select paymentLastBillingPeriod, paymentThisBillingPeriod, pendingBalance from accounts where accountNumber = ?", (self.accountNumber,)).fetchone()

        paymentEntered = float(paymentEntered)

        if chosenFunction == payAll:

            if paymentEntered < paymentFetch[2]:
                messagebox.showinfo("Error!", "Insufficient amount!")

            elif paymentEntered > paymentFetch[2]:
                paymentChange = paymentEntered - paymentFetch[2]
                messagebox.showinfo("Change!", f"Here is your change: {paymentChange}")
                messagebox.showinfo("Payment successful!", "Payment successful! Thank you!")
                payAll(self.accountNumber)
                self.payWindow.destroy()

            elif paymentEntered == paymentFetch[2]:
                messagebox.showinfo("Payment successful!", "Payment successful! Thank you!")
                payAll(self.accountNumber)
                self.payWindow.destroy()

        if chosenFunction == payOnlyLastMonth:
            
            if paymentEntered < paymentFetch[0]:
                messagebox.showinfo("Error!", "Insufficient amount!")

            elif paymentEntered > paymentFetch[0]:
                paymentChange = paymentEntered - paymentFetch[0]
                messagebox.showinfo("Change!", f"Here is your change: {paymentChange}")
                messagebox.showinfo("Payment successful!", "Payment successful! Thank you!")
                payOnlyLastMonth(self.accountNumber)
                self.payWindow.destroy()

            elif paymentEntered == paymentFetch[0]:
                messagebox.showinfo("Payment successful!", "Payment successful! Thank you!")
                payOnlyLastMonth(self.accountNumber)
                self.payWindow.destroy()
    ###        
    def viewTransactionHistory(self):
        self.clearContent()

        historyFrame = tk.Frame(self.contentFrame, bg = '#ffffff', bd = 2, relief = 'solid') 
        historyFrame.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")

        tk.Label(historyFrame, 
                 text = "Transaction History Page", 
                 font = ("Arial", 24), 
                 bg =  "#ffffff").pack(pady = 20)
        
        textFont = ("Arial", 14)

        historyBody = tk.Text(historyFrame, height = 17, width = 50, font = textFont)

        scrollBar = tk.Scrollbar(historyFrame, command = historyBody.yview)

        historyBody.configure(yscrollcommand = scrollBar.set)

        historyBody.pack(side = 'left')
        scrollBar.pack(side = 'right', fill = 'y')

        historyBody.config(state = 'disabled')
        self.bellIconSwitch()

    def logout(self):
        from loginWindow import loginWindow
        self.mainWindow.destroy()
        loginWindow()

    def clearContent(self):
        '''
        helper function to clear widgets
        before adding the new widgets
        when switching between pages
        '''
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

    def notificationButton(self):
        paymentStatusCheck = self.cursor.execute("select paymentStatus, paymentThisBillingPeriod, pendingBalance from accounts where accountNumber = ?", (self.accountNumber,)).fetchone()
        if paymentStatusCheck[0] == 'unpaid' and paymentStatusCheck[2]:

            messagebox.showinfo("Notification!", "A new bill is available!")
            self.cursor.execute("update notifications set viewed = 'true' where accountNumber = ?", (self.accountNumber,))
            self.connection.commit()
        else:
            messagebox.showinfo("Notification!", "There are currently no notifications!")

        self.bellIconSwitch()
        # self.mainPage()

    def bellIconSwitch(self):
        '''
        helper function that continuously checks 
        every time if a notification is available,
        this function gets called every time a user clicks a button
        '''
        bellFrame = tk.Frame(self.mainWindow, bg = "#bbbbbb")
        bellFrame.grid(row = 0, column = 1, sticky = "ne", padx = 20, pady = 20)

        # this serves as a flag to determine if the user has already viewed their notifications or not
        # the notifcations table updates every time a bill is generated
        self.viewedNotification = self.cursor.execute("select viewed from notifications where accountNumber = ?", (self.accountNumber,)).fetchone()

        if self.viewedNotification[0] == 'true':
            img = Image.open("images/defaultBell.png")
        
        else:
            img = Image.open("images/notifiedBell.png")
        

        img = img.resize((80, 80))
        self.bellIcon = ImageTk.PhotoImage(img)  
        tk.Button(bellFrame,
                  image = self.bellIcon,
                  fg = "#bbbbbb",
                  bg = "#bbbbbb",
                  bd = 0,
                  activebackground = "#bbbbbb",
                  width = 50,
                  height = 50,
                  command = self.notificationButton).pack()
