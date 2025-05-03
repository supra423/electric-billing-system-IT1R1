import tkinter as tk

from databaseTables import Database


class mainMenu(Database):
    def __init__(self):
        self.mainWindow = tk.Tk()
        self.mainWindow.title("Main Menu")
        self.mainWindow.minsize(800, 500)
        self.mainWindow.configure(bg = "#aaaaaa")

        self.sideBar = tk.Frame(self.mainWindow, bg = '#2c3e50', width = 200)
        self.sideBar.pack(side = 'left', fill = 'y')
         
        self.mainButtons("1", self.passFunction)
        self.mainButtons("2", self.passFunction)
        self.mainButtons("3", self.passFunction)
        self.mainButtons("4", self.passFunction)

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
                  fg = "#ffffff").pack(pady = 10, fill = "x" )
        
    def passFunction(self):
        pass
                


window = mainMenu()
