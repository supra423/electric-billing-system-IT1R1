import subprocess
import sys

import psutil


def isProcessRunning(scriptName):

    for proc in psutil.process_iter(attrs = ['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'python.exe' and scriptName in ' '.join(proc.info['cmdline']):
            return True

    return False

scriptPath = 'kwh.py'

if not isProcessRunning(scriptPath):
    subprocess.Popen([sys.executable, scriptPath], creationflags=subprocess.DETACHED_PROCESS)
else:
    print("kWh process is already running!")
