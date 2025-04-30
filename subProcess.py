import os
import subprocess
import sys

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

            else:
                print("You are not running in windows!")
                return

        else:
            print(f"{self.scriptName} is already running!")
