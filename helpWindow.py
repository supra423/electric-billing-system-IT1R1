import tkinter as tk
from tkinter import messagebox

class helpWindow():
    def __init__(self, whichWindow):

        self.whichWindow = whichWindow

        self.helpWindow = tk.Tk()
        self.helpWindow.title("Help?")
        self.helpWindow.geometry("500x500")
        self.helpWindow.configure(bg = "#bbbbbb")
        self.helpWindow.resizable(False, False)

        self.helpWindow.rowconfigure(0, weight = 1)
        self.helpWindow.columnconfigure(1, weight = 1)

        self.helpFrame = tk.Frame(self.helpWindow,
                                  bg = "#bbbbbb",
                                  relief = "solid",
                                  height = 20,
                                  width = 40)

        self.helpFrame.grid(row = 0, column = 0, padx = 45)

        self.helpFrame.rowconfigure(0, weight = 1)
        self.helpFrame.columnconfigure(0, weight = 1)

        self.helpBody = tk.Text(self.helpFrame,
                                height = 20,
                                width = 35,
                                font = ("Arial", 14),
                                bg = "#ffffff")
        self.helpBody.grid(row = 0, column = 0)

        self.scrollBar = tk.Scrollbar(self.helpFrame,
                                 command = self.helpBody.yview)

        self.helpBody.configure(yscrollcommand = self.scrollBar.set)

        self.scrollBar.grid(row = 0, column = 1, sticky = "ns", rowspan = 3)

        if self.whichWindow == "loginWindow":
            self.loginWindowHelp()

        elif self.whichWindow == "createAccount":
            self.createAccountHelp()

        elif self.whichWindow == "windowMain":
            self.windowMainHelp()

        def loginWindowHelp(self):
            with open("helpLoginWindowText.txt", "r") as file:
                fetchedText = file.read()

            helpBody.insert('1.0', f"{fetchedText}\n")

        def createAccountHelp(self):
            pass

        def windowMainHelp(self):
            pass

        self.helpWindow.bind('<Escape>', lambda event: self.helpWindow.destroy())

        self.helpWindow.mainloop()
