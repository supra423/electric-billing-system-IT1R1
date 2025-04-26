import tkinter as tk


class mainMenu:
    def __init__(self):
        self.mainWindow = tk.Tk()
        self.mainWindow.title("Main Menu")
        self.mainWindow.geometry("1000x700")

        self.label1 = tk.Label(self.mainWindow, 
                        text = "Epalco", 
                        font=("Arial", 20))
        self.label1.pack(side="top", 
                    anchor = "w", 
                    padx = 30, 
                    pady = 30)

        # insert left frame

        self.leftFrame = tk.Frame(self.mainWindow)
        self.leftFrame.pack(side = "left", 
                    padx = 15, 
                    pady = 30, 
                    expand = True, 
                    fill = "both")

        self.leftFrame.grid_rowconfigure(0, weight = 1)
        self.leftFrame.grid_rowconfigure(1, weight = 0)
        self.leftFrame.grid_columnconfigure((0, 1), weight = 1)

        self.button1 = tk.Button(self.leftFrame, 
                            text = "Button 1", 
                            font = ("Arial", 15))
        self.button1.grid(row = 0, 
                    column = 0, 
                    padx = 20, 
                    pady = 10, 
                    sticky = "sew")

        self.button2 = tk.Button(self.leftFrame, 
                            text="Button 2", 
                            font=("Arial", 15))
        self.button2.grid(row = 0, 
                    column = 1, 
                    padx = 20, 
                    pady = 10, 
                    sticky = "sew")

        # insert right frame

        self.rightFrame = tk.Frame(self.mainWindow)
        self.rightFrame.pack(side = "right", 
                        anchor = "s", 
                        padx = 10, 
                        pady = 30, 
                        expand = True, 
                        fill = "both")

        self.rightFrame.grid_rowconfigure(0, weight = 1)
        self.rightFrame.grid_rowconfigure(1, weight = 0)
        self.rightFrame.grid_columnconfigure((0, 1), weight = 1)

        self.button3 = tk.Button(self.rightFrame, 
                            text = "Button 3", 
                            font = ("Arial", 15))
        self.button3.grid(row = 0, 
                    column = 0, 
                    padx = 20, 
                    pady = 10, 
                    sticky = "sew")

        self.button4 = tk.Button(self.rightFrame, 
                            text = "Button 4", 
                            font = ("Arial", 15))
        self.button4.grid(row = 0, 
                    column = 1, 
                    padx = 20, 
                    pady = 10, 
                    sticky = "sew")

        self.mainWindow.mainloop()

