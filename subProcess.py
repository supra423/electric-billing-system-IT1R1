import os
import subprocess
import sys
from tkinter import messagebox

import psutil

# It checks if the script is already running, and if not, launches it.
class subProcess:
    def __init__(self, scriptname):
        self.scriptname = scriptname
        self.startprocess()

    def isprocessrunning(self):
        for proc in psutil.process_iter(attrs = ['pid', 'name', 'cmdline']):

            try:
                if proc.info['name'] == 'python.exe' and self.scriptname in ' '.join(proc.info['cmdline']):
                    return proc.info['pid'] 

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return None

    def startprocess(self):
        pid = self.isprocessrunning()
        if os.name == 'nt' and pid is None:
            process = subprocess.Popen([sys.executable, self.scriptname], creationflags = subprocess.DETACHED_PROCESS)
       
            print(f"{self.scriptname} is running! PID: {process.pid}") # printing the PID is for debugging purposes

        # If not on Windows, show an error and stop execution
        elif os.name != 'nt':
            messagebox.showinfo("error!", "you must be running on windows!")
            raise Exception
    
        # If script is already running, just print its PID
        elif pid:
            print(f"{self.scriptname} is already running! PID: {pid}")


