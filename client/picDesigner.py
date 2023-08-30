import tkinter as tk
from tkinter import ttk

class PictureViewer(tk.Toplevel):  
    def __init__(self, master=None): 
        super().__init__(master) 

        self.title("Picture Viewer")
        self.geometry("600x450")

        self.picture_frame = tk.Frame(self)
        self.picture_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.picture = tk.Label(self.picture_frame)
        self.picture.pack(fill=tk.BOTH, expand=True)
        
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.butTake = ttk.Button(self.button_frame, text="Capture", command=self.butTake_Click)
        self.butTake.pack(side=tk.LEFT, padx=5)
        
        self.button1 = ttk.Button(self.button_frame, text="Save", command=self.button1_Click)
        self.button1.pack(side=tk.LEFT, padx=5)
        
        self.protocol("WM_DELETE_WINDOW", self.pic_closing)
