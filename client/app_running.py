import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import socket

class AppRunningController:
    def __init__(self, client):
        self.client = client
        self.app = tk.Tk()
        self.app.title("App Running")
        self.app.configure(bg="white")

        self.create_ui()

    def create_ui(self):
        start_button = tk.Button(self.app, text="Start", bg="#E6E9D0", activebackground='#bec0b1', font="Helvetica 11 bold", padx=30, pady=20, command=self.start_app, bd=5)
        start_button.grid(row=0, column=0, padx=8)

        watch_button = tk.Button(self.app, text="Watch", bg="#F9BDC0", activebackground='#7e5a5c', font="Helvetica 11 bold", padx=30, pady=20, command=self.watch_app, bd=5)
        watch_button.grid(row=0, column=1, padx=8)

        kill_button = tk.Button(self.app, text="Kill", bg="#8DDDE0", activebackground='#497172', font="Helvetica 11 bold", padx=30, pady=20, command=self.kill_app, bd=5)
        kill_button.grid(row=0, column=2, padx=8)

        delete_button = tk.Button(self.app, text="Delete", bg="#FBE698", activebackground='#776d47', font="Helvetica 11 bold", padx=30, pady=20, command=self.clear_ui, bd=5)
        delete_button.grid(row=0, column=3, padx=8)

    def start_app(self):
        name_input = self.show_input_dialog("Start", "Nhập tên")
        if name_input:
            self.send_command("OpenTask", name_input, "opened", "Không tìm thấy chương trình")

    def watch_app(self):
        try:
            self.send_command("Watch_AppRunning")
            length = int(self.client.recv(1024).decode("utf-8"))

            app_info = []
            for _ in range(length):
                data = self.client.recv(1024).decode("utf-8")
                app_info.append(data)
                self.client.sendall(bytes(data, "utf-8"))

            self.show_app_list(app_info)
        except:
            self.show_connection_error()

    def kill_app(self):
        name_input = self.show_input_dialog("Kill", "Nhập tên")
        if name_input:
            self.send_command("Kill_Task", name_input, "Da xoa tac vu", "Không tìm thấy chương trình")

    def clear_ui(self):
        self.app_activity.destroy()

    def send_command(self, cmd, param="", success_response="", error_response=""):
        try:
            self.client.sendall(bytes(cmd, "utf-8"))
            self.client.sendall(bytes(param, "utf-8"))
            response = self.client.recv(1024).decode("utf-8")
            if response == success_response:
                messagebox.showinfo("", success_response)
            else:
                messagebox.showinfo("Error !!!", error_response)
        except:
            self.show_connection_error()

    def show_app_list(self, app_info):
        self.app_activity = tk.Frame(self.app, bg="white", padx=20, pady=20, borderwidth=5)
        self.app_activity.grid(row=1, columnspan=5, padx=20)

        scrollbar = tk.Scrollbar(self.app_activity)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        content_treeview = ttk.Treeview(self.app_activity, yscrollcommand=scrollbar.set)
        content_treeview.pack()
        scrollbar.config(command=content_treeview.yview)

        content_treeview["columns"] = ("1", "2")
        content_treeview.column("#0", anchor=tk.CENTER, width=200, minwidth=25)
        content_treeview.column("1", anchor=tk.CENTER, width=100)
        content_treeview.column("2", anchor=tk.CENTER, width=100)

        content_treeview.heading("#0", text="App Name", anchor=tk.W)
        content_treeview.heading("1", text="ID", anchor=tk.CENTER)
        content_treeview.heading("2", text="Thread", anchor=tk.CENTER)

        for i, data in enumerate(app_info):
            app_name, app_id, app_thread = data.split(",")
            content_treeview.insert(parent='', index='end', iid=i, text=app_name, values=(app_id, app_thread))

    def show_input_dialog(self, title, label_text):
        screen = tk.Tk()
        screen.geometry("320x50")
        screen.title(title)
        name_input = tk.Entry(screen, width=35)
        name_input.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        name_input.insert(tk.END, label_text)
        button = tk.Button(screen, text=title, bg="#FFE4E1", font="Helvetica 10 bold", padx=20, command=screen.quit, bd=5, activebackground='#877776')
        button.grid(row=0, column=4, padx=5, pady=5)
        screen.mainloop()
        return name_input.get()

    def show_connection_error(self):
        messagebox.showinfo("Error !!!", "Lỗi kết nối")

class Main:
    def __init__(self):
        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.home = tk.Tk()
        self.home.withdraw()
        self.home.configure(bg="#FFFAF0")
        self.login_window()

    def login_window(self):
        login = tk.Toplevel()
        login.configure(bg="#fff")
        login.title("Login")
        login.geometry("650x650")
        login.resizable(False, False)
        label_ip = tk.Label(login, text="Nhập địa chỉ IP để tiếp tục:", compound="center", bg="#FFFEEC", font="Helvetica 15 bold")
        label_ip.place(relx=0.05, rely=0.05)
        input_ip = tk.Entry(login, bg="#FFF0F5", font="Helvetica 14")
        input_ip.insert(tk.END, self.server_ip)
        input_ip.place(relx=0.501, rely=0.05)
        input_ip.focus()
        connect_button = tk.Button(login, text="Kết nối", width=20, bg="#A3E4DB", font="Helvetica 15 bold", command=self.connect_to_server, bd=5, activebackground='#2f4e5a')
        connect_button.place(relx=0.3, rely=0.18)

    def connect_to_server(self):
        server_ip = self.input_ip.get()
        self.login_window_instance.destroy()
        self.start_client(server_ip)

    def start_client(self, server_ip):
        port = 1234
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server_ip, port))
            messagebox.showinfo("Successful !!!", "Kết nối server thành công")
            app_running_controller = AppRunningController(client)
            self.home.mainloop()
        except:
            messagebox.showinfo("Error!!!", "Không thể kết nối đến server")

if __name__ == "__main__":
    main = Main()
