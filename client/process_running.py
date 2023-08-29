import tkinter as tk
from tkinter import messagebox

class ProcessListGUI:
    def __init__(self, title, client, server_connect):
        self.client = client
        self.s = server_connect

        self.process_list_window = tk.Toplevel()
        self.process_list_window.title(title)

        self.process_text = tk.Text(self.process_list_window, wrap=tk.WORD)
        self.process_text.pack()

        self.input_id_process_field = tk.Entry(self.process_list_window)
        self.input_id_process_field.pack()

        self.start_button = tk.Button(self.process_list_window, text="Start", command=self.start_action)
        self.start_button.pack()

        self.kill_button = tk.Button(self.process_list_window, text="Kill", command=self.kill_action)
        self.kill_button.pack()

        self.exit_button = tk.Button(self.process_list_window, text="Exit", command=self.exit_action)
        self.exit_button.pack()

    def render_process_area(self, data):
        self.process_text.delete(1.0, tk.END)
        self.process_text.insert(tk.END, data)

    def start_action(self):
        name_process = self.input_id_process_field.get()
        try:
            self.client.send_message("Start")
            self.client.send_message(name_process)
            request = self.client.get_client_recv_message()
            messagebox.showinfo("Start", request)
            process_list_update = self.client.get_client_recv_message()
            self.render_process_area(process_list_update)
        except Exception as e:
            print("Error:", e)

    def kill_action(self):
        id_kill = self.input_id_process_field.get()
        try:
            self.client.send_message("Kill")
            self.client.send_message(id_kill)
            request = self.client.get_client_recv_message()
            messagebox.showinfo("Kill", request)
            process_list_update = self.client.get_client_recv_message()
            self.render_process_area(process_list_update)
        except Exception as e:
            print("Error:", e)

    def exit_action(self):
        try:
            self.client.send_message("Exit")
            self.client.send_message("Exit")
            self.process_list_window.destroy()
        except Exception as e:
            print("Error:", e)
