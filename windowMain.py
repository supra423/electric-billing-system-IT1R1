import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
from databaseTables import Database


class mainMenu():
    def __init__(self):

        self.connection = sqlite3.connect('database.s3db')
        self.cursor = self.connection.cursor()

        self.mainWindow = tk.Tk()
        self.mainWindow.title("Main Menu")
        self.mainWindow.minsize(1000, 700)
        self.mainWindow.configure(bg = "#aaaaaa")

        self.sideBar = tk.Frame(self.mainWindow, bg = '#2c3e50', width = 200)
        self.sideBar.pack(side = 'left', fill = 'y')
        
        # main menu button
        tk.Button(self.sideBar,
                  text = "E P A L C O",
                  width = 10,
                  height = 1,
                  bg = "#2c3e50",
                  activebackground = "#2c3e50",
                  bd = 0,
                  fg = "#ffffff",
                  font = ("Arial", 16, "bold")).pack(pady = 10)
        
        img = Image.open("images/bell-icon.png")
        img = img.resize((40, 40))
        bellIcon = ImageTk.PhotoImage(img)
        tk.Button(self.mainWindow,
                  image = bellIcon,
                  fg = "#aaaaaa",
                  bg = "#aaaaaa",
                  bd = 0,
                  activebackground = "#aaaaaa",
                  width = 50,
                  height = 50).pack(pady = 20, padx = 20, anchor = "ne")

        self.mainButtons("Generate Bill", self.passFunction)
        self.mainButtons("Pay", self.passFunction)
        self.mainButtons("View transaction history", self.passFunction)
        self.mainButtons("Logout", self.passFunction)

        self.mainWindow.mainloop()

    def mainButtons(self, buttonText, buttonCommand):
        ' helper function for making buttons '
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
        
    def passFunction(self):
        pass
