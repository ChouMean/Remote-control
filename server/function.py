import subprocess
import os
import mss
import mss.tools
import time
from PIL import ImageGrab

class Function:
    def get_process_list(self):
        command = "powershell.exe gps | select ProcessName,Id,Description"
        cmd_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = cmd_process.communicate()
        return stdout.decode()

    def kill_process(self, pid):
        process_list = self.get_process_list()
        if pid not in process_list:
            return "Fail"
        
        command = f"taskkill /F /PID {pid}"
        try:
            subprocess.run(command, shell=True, check=True)
            return "Success"
        except subprocess.CalledProcessError:
            return "Fail"

    def get_application_list(self):
        command = "powershell.exe gps | where {$_.MainWindowTitle } | select ProcessName,Id,Description"
        cmd_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = cmd_process.communicate()
        return stdout.decode()

    def start_application(self, application_name):
        command = f"Start-Process {application_name}"
        try:
            subprocess.run(["powershell.exe", command], shell=True, check=True)
            return "Success"
        except subprocess.CalledProcessError:
            return "Fail"

    def kill_application(self, pid):
        application_list = self.get_application_list()
        if pid not in application_list:
            return "Fail"

        command = f"taskkill /F /PID {pid}"
        try:
            subprocess.run(command, shell=True, check=True)
            return "Success"
        except subprocess.CalledProcessError:
            return "Fail"

    def capture_screen(self):
        screenshot_path = "captureScreen.png"
        with mss.mss() as sct:
            screenshot = sct.shot(output=screenshot_path)

    def turn_off(self):
        command = "shutdown -s -t 1"
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    function = Function()
    # You can call the methods of the Function class here
