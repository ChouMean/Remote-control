import tkinter as tk
from tkinter import ttk

class KillApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Kill Application")
        self.geometry("300x100")
        
        self.configure(bg="white")
        
        self.label = ttk.Label(self, text="Enter ID:")
        self.label.pack(pady=10)
        
        self.txtID = ttk.Entry(self)
        self.txtID.pack(pady=5)
        
        self.butNhap = ttk.Button(self, text="Kill", command=self.butNhap_Click)
        self.butNhap.pack()
        
        self.protocol("WM_DELETE_WINDOW", self.kill_closing)
