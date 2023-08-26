import tkinter as tk
from tkinter import messagebox
import socket
import threading
import os
from io import BytesIO
from PIL import ImageGrab

class Client:
    def __init__(self):
        self.s = None
        self.bufferedReader = None
        self.dataOutputStream = None
        self.create_window(400, 250)
        self.init_actions()

    def create_window(self, w, h):
        self.main_frame = tk.Tk()
        self.main_frame.title("Client")

        tk.Label(self.main_frame, text="Server IP:").pack(pady=10)
        self.ip_input = tk.Entry(self.main_frame)
        self.ip_input.pack()

        self.connect_button = tk.Button(self.main_frame, text="Connect", command=self.create_client)
        self.connect_button.pack(pady=10)

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        self.process_running_button = tk.Button(button_frame, text="Running Processes", command=self.process_running)
        self.app_running_button = tk.Button(button_frame, text="Running Apps", command=self.app_running)
        self.capture_screen_button = tk.Button(button_frame, text="Capture Screen", command=self.capture_screen)
        self.key_logger_button = tk.Button(button_frame, text="Key Logger", command=self.key_logger)
        self.shutdown_button = tk.Button(button_frame, text="Shutdown", command=self.shutdown)
        self.exit_button = tk.Button(button_frame, text="Exit", command=self.exit)

        self.process_running_button.grid(row=0, column=0, padx=10, pady=5)
        self.app_running_button.grid(row=0, column=1, padx=10, pady=5)
        self.capture_screen_button.grid(row=0, column=2, padx=10, pady=5)
        self.key_logger_button.grid(row=1, column=0, padx=10, pady=5)
        self.shutdown_button.grid(row=1, column=1, padx=10, pady=5)
        self.exit_button.grid(row=1, column=2, padx=10, pady=5)

        self.main_frame.geometry(f"{w}x{h}")
        self.main_frame.resizable(False, False)
        self.main_frame.mainloop()


    def init_actions(self):
        self.client = self

    def create_client(self):
        try:
            ip = self.ip_input.get()
            if ip == socket.gethostbyname(socket.gethostname()):
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((ip, 80))
                self.bufferedReader = self.s.makefile("rb")
                self.dataOutputStream = self.s.makefile("wb")
                messagebox.showinfo("Information", "Server Connected!")
            else:
                messagebox.showwarning("ERROR", "Can't Connect")
        except Exception as e:
            messagebox.showwarning("ERROR", str(e))

    def process_running(self):
        try:
            self.send_message("PROCESS")
            process_list = self.get_client_recv_message()
            process_list_gui = ProcessListGUI("Show Process", self.client, self.s)
            process_list_gui.render_process_area(process_list)
        except Exception:
            messagebox.showwarning("ERROR", "No server connected")

    def app_running(self):
        try:
            self.send_message("APP")
            process_list = self.get_client_recv_message()
            process_list_gui = ProcessListGUI("Show Process", self.client, self.s)
            process_list_gui.render_process_area(process_list)
        except Exception:
            messagebox.showwarning("ERROR", "No server connected")

    def key_logger(self):
        try:
            self.send_message("KEYLOGGER")
            key_logger = KeyLogger(self.client)
            key_logger.title("Key Logger")
        except Exception:
            messagebox.showwarning("ERROR", "No server connected")

    def capture_screen(self):
        try:
            self.send_message("CAPTURE")
            file_name = "captureScreen.png"
            self.get_file_screen(file_name)
            messagebox.showinfo("Capture Screen", "Successfully!")
        except Exception:
            messagebox.showwarning("ERROR", "No server connected")

    def shutdown(self):
        try:
            self.send_message("SHUTDOWN")
        except Exception:
            messagebox.showwarning("ERROR", "No server connected")

    def exit(self):
        try:
            self.send_message("OUT")
            self.dataOutputStream.close()
            self.s.close()
        except Exception:
            pass
        finally:
            self.main_frame.destroy()

    def send_message(self, message):
        try:
            self.dataOutputStream.write(message.encode())
            self.dataOutputStream.write(b"\nEnd message\n")
            self.dataOutputStream.flush()
        except Exception as e:
            print("Error:", e)

    def get_client_recv_message(self):
        data_message = ""
        while True:
            get_line = self.bufferedReader.readline().decode().strip()
            if get_line == "End message":
                break
            if data_message == "":
                data_message = get_line
            else:
                data_message += "\n" + get_line
        return data_message

    def get_file_screen(self, file_name):
        with open(file_name, "wb") as file_output:
            while True:
                byte_list = self.bufferedReader.read(1024)
                file_output.write(byte_list)
                if len(byte_list) < 1024:
                    break

class ProcessListGUI:
    def __init__(self, title, client, socket):
        self.client = client
        self.s = socket
        self.process_list_window = tk.Toplevel()
        self.process_list_window.title(title)

        self.process_text = tk.Text(self.process_list_window, wrap=tk.WORD)
        self.process_text.pack()

    def render_process_area(self, process_list):
        self.process_text.delete(1.0, tk.END)
        self.process_text.insert(tk.END, process_list)

class KeyLogger(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.title("Key Logger")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.text = tk.Text(self)
        self.text.pack()
        self.key_log = ""
        self.bind("<Key>", self.key_pressed)

    def key_pressed(self, event):
        key = event.keysym
        self.key_log += key
        self.text.insert(tk.END, key)

    def on_close(self):
        self.client.send_message("KEYLOG " + self.key_log)
        self.destroy()

if __name__ == "__main__":
    Client()
