import socket

import tkinter as tk

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client")
        self.root.geometry("400x400")

        self.custom_font = ("Helvetica", 9)

        get_ip = socket.gethostbyname(socket.gethostname())
        self.txtIP = self.create_entry(get_ip, 20, 20, 260, 25)
        self.butConnect = self.create_button("Connect", self.connect_server, 300, 20, 80, 25)

        self.butApp = self.create_button("App Running", self.run_app, 20, 60, 120, 80)
        self.butTat = self.create_button("Shutdown", self.shutdown, 160, 60, 120, 80)
        self.butKeyLock = self.create_button("KeyLogger", self.keylogger, 300, 60, 80, 80)

        self.butReg = self.create_button("Registry", self.edit_registry, 20, 180, 120, 80)
        self.butPic = self.create_button("Screenshot", self.screen_capture, 160, 180, 120, 80)
        self.butProcess = self.create_button("Process\nRunning", self.run_process, 300, 180, 80, 80)

        self.butExit = self.create_button("Exit", self.exit_app, 160, 295, 90, 75)


    def create_button(self, text, command, x, y, width, height):
        button = tk.Button(self.root, text=text, font=self.custom_font, command=command, relief=tk.GROOVE)
        button.place(x=x, y=y, width=width, height=height)
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)
        return button

    def create_entry(self, default_text, x, y, width, height):
        entry = tk.Entry(self.root)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, default_text)
        return entry

    def on_enter(self, event):
        event.widget.config(bg="#e6e6fa")

    def on_leave(self, event):
        event.widget.config(bg="SystemButtonFace")

    def run_app(self):
        pass

    def connect_server(self):
        pass

    def shutdown(self):
        pass

    def edit_registry(self):
        pass

    def exit_app(self):
        pass

    def take_screenshot(self):
        pass

    def keylogger(self):
        pass

    def run_process(self):
        pass