import os
import subprocess
import sys
from tkinter import messagebox

import psutil


class subProcess:
    def __init__(self, scriptName):
        self.scriptName = scriptName
        self.startProcess()

    def isProcessRunning(self):
        for proc in psutil.process_iter(attrs = ['pid', 'name', 'cmdline']):

            try:
                if proc.info['name'] == 'python.exe' and self.scriptName in ' '.join(proc.info['cmdline']):
                    return True

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return False

    def startProcess(self):
        if not self.isProcessRunning():

            if os.name == 'nt':
                subprocess.Popen([sys.executable, self.scriptName], creationflags = subprocess.DETACHED_PROCESS)
                print(f"{self.scriptName} is running!")
            else:
                #print("You are not running in windows!")
                messagebox.showinfo("Error!", "You must be running on windows!")
                raise Exception
        
        else:
            print(f"{self.scriptName} is already running!")
