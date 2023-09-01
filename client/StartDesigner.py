import tkinter as tk
from tkinter import ttk

class Start(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Start")
        self.geometry("300x100")

        self.configure(bg="white")
        
        self.label = ttk.Label(self, text="Enter app name:")
        self.label.pack(pady=10)
        
        self.txtID = ttk.Entry(self)
        self.txtID.pack(pady=5)
        
        self.butNhap = ttk.Button(self, text="Start", command=self.butStart_Click)
        self.butNhap.pack()
        
        self.protocol("WM_DELETE_WINDOW", self.start_closing)
    
    