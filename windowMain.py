import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


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
        self.mainWindow.configure(bg = "#aaaaaa")

        # Configure the grid layout of the main window
        self.mainWindow.rowconfigure(0, weight=1)
        self.mainWindow.columnconfigure(1, weight=1)

        # Sidebar (column 0)
        self.sideBar = tk.Frame(self.mainWindow, bg = '#2c3e50', width = 200)
        self.sideBar.grid(row = 0, column = 0, sticky = "ns")

        # Content frame (column 1)
        self.contentFrame = tk.Frame(self.mainWindow, bg = "#aaaaaa")
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

        bell_frame = tk.Frame(self.mainWindow, bg = "#aaaaaa")
        bell_frame.grid(row = 0, column = 1, sticky = "ne", padx = 20, pady = 20)

        # this serves as a flag to determine if the user has already viewed their notifications or not
        # the notifcations table updates every time a bill is generated
        self.viewedNotification = self.cursor.execute("select viewed from notifications where accountNumber = ?", (self.accountNumber,)).fetchone()

        if self.viewedNotification[0] == 'true':
            img = Image.open("images/defaultBell.png")
        
        else:
            img = Image.open("images/notifiedBell.png")
        

        img = img.resize((80, 80))
        self.bellIcon = ImageTk.PhotoImage(img)  
        tk.Button(bell_frame,
                  image = self.bellIcon,
                  fg = "#aaaaaa",
                  bg = "#aaaaaa",
                  bd = 0,
                  activebackground = "#aaaaaa",
                  width = 50,
                  height = 50,
                  command = self.notificationButton).pack()

        content = tk.Frame(self.contentFrame, bg = "#aaaaaa")
        content.grid(row = 1, column = 0, columnspan = 2, sticky = "nw", padx = 20, pady = 20)

        tk.Label(content,
                 text = "Welcome!",
                 font = ("Arial", 40),
                 bg = "#aaaaaa").pack(anchor = "nw")
        tk.Label(content,
                 text = self.username,
                 font = ("Arial", 40),
                 bg = "#aaaaaa").pack(anchor = "nw")

    def generateBill(self):
        self.clearContent()

        billFrame = tk.Frame(self.contentFrame, bg = "white", bd = 2, relief = "solid")
        billFrame.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")

        tk.Label(billFrame,
                 text = "Your Bill",
                 font = ("Arial", 20),
                 bg = "white").pack(pady = 20)


    def pay(self):
        self.clearContent()
        tk.Label(self.contentFrame, text = "Pay Page", font = ("Arial", 24), bg = "#aaaaaa").grid(row = 0, column = 0, padx = 20, pady = 20)

    def viewTransactionHistory(self):
        self.clearContent()
        tk.Label(self.contentFrame, text = "Transaction History Page", font = ("Arial", 24), bg =  "#aaaaaa").grid(row = 0, column = 0, padx = 20, pady = 20)

    def logout(self):
        from loginWindow import accountLogin
        self.mainWindow.destroy()
        accountLogin()

    def clearContent(self):
        '''
        helper function to clear widgets
        before adding the new widgets
        when switching between pages
        '''
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
    def notificationButton(self):
        if self.viewedNotification[0] == 'false':

            messagebox.showinfo("Notification!", "A new bill is available!")
            self.cursor.execute("update notifications set viewed = 'true' where accountNumber = ?", (self.accountNumber,))
            self.connection.commit()
        else:
            messagebox.showinfo("Notification!", "There are currently no notifications!")
            

        self.clearContent()
        self.mainPage()

    def passFunction(self):
        pass
