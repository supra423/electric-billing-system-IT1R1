import sqlite3
import tkinter as tk
from PIL import Image, ImageTk


class mainMenu():

    def __init__(self, user):

        self.username = user[0]
        self.accountNumber = user[1]
        self.address = user[2]

        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()

        self.mainWindow = tk.Tk()
        self.mainWindow.title("Main Menu")
        self.mainWindow.minsize(1000, 700)
        self.mainWindow.configure(bg="#aaaaaa")

        # Configure the grid layout of the main window
        self.mainWindow.rowconfigure(0, weight=1)
        self.mainWindow.columnconfigure(1, weight=1)

        # Sidebar (column 0)
        self.sideBar = tk.Frame(self.mainWindow, bg='#2c3e50', width=200)
        self.sideBar.grid(row=0, column=0, sticky="ns")

        # Content frame (column 1)
        self.contentFrame = tk.Frame(self.mainWindow, bg="#aaaaaa")
        self.contentFrame.grid(row=0, column=1, sticky="nsew")

        #  buttons
        tk.Button(self.sideBar,
                  text="E P A L C O",
                  width=10,
                  height=1,
                  bg="#2c3e50",
                  activebackground="#2c3e50",
                  bd=0,
                  fg="#ffffff",
                  font=("Arial", 16, "bold"),
                  command=self.mainPage).pack(pady=10)

        self.mainButtons("Generate Bill", self.generateBill)
        self.mainButtons("Pay", self.pay)
        self.mainButtons("View transaction history", self.viewTransactionHistory)
        self.mainButtons("Logout", self.logout)

        self.mainPage() 

        self.mainWindow.mainloop()

    def mainButtons(self, buttonText, buttonCommand):
        tk.Button(self.sideBar,
                  text=buttonText,
                  width=20,
                  height=2,
                  activebackground="#7baee0",
                  command=buttonCommand,
                  anchor="w",
                  padx=10,
                  bg="#3f5a75",
                  fg="#ffffff",
                  font=("Arial", 16)).pack(pady=10, fill="x")

    def mainPage(self):
        self.clearContent()

        bell_frame = tk.Frame(self.mainWindow, bg="#aaaaaa")
        bell_frame.grid(row=0, column=1, sticky="ne", padx=20, pady=20)

        img = Image.open("images/notifiedBell.png")
        img = img.resize((80, 80))
        self.bellIcon = ImageTk.PhotoImage(img)  
        tk.Button(bell_frame,
                  image=self.bellIcon,
                  fg="#aaaaaa",
                  bg="#aaaaaa",
                  bd=0,
                  activebackground="#aaaaaa",
                  width=50,
                  height=50).pack()

        content = tk.Frame(self.contentFrame, bg="#aaaaaa")
        content.grid(row=1, column=0, columnspan=2, sticky="nw", padx=20, pady=20)

        tk.Label(content,
                 text="Welcome!",
                 font=("Arial", 40),
                 bg="#aaaaaa").pack(anchor="nw")
        tk.Label(content,
                 text=self.username,
                 font=("Arial", 40),
                 bg="#aaaaaa").pack(anchor="nw")

    def generateBill(self):
        self.clearContent()

        billFrame = tk.Frame(self.contentFrame, bg="white", bd=2, relief="solid")
        billFrame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        tk.Label(billFrame,
                 text="Your Billasd\nasdasdasdnasd\nfsdfasdfsdina\ndasdasd",
                 font=("Arial", 20),
                 bg="white").pack(pady=20)


    def pay(self):
        self.clearContent()
        tk.Label(self.contentFrame, text="Pay Page", font=("Arial", 24), bg="#aaaaaa").grid(row=0, column=0, padx=20, pady=20)

    def viewTransactionHistory(self):
        self.clearContent()
        tk.Label(self.contentFrame, text="Transaction History Page", font=("Arial", 24), bg="#aaaaaa").grid(row=0, column=0, padx=20, pady=20)

    def logout(self):
        from loginWindow import accountLogin
        self.mainWindow.destroy()
        accountLogin()

    def clearContent(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

    def passFunction(self):
        pass
