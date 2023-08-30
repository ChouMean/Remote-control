import tkinter as tk
from tkinter import scrolledtext, Button

class KeylogApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("KeyLogger")
        self.geometry("400x500")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.txtKQ = scrolledtext.ScrolledText(self, wrap=tk.WORD, state="disabled")
        self.txtKQ.pack(fill="both", expand=True, padx=10, pady=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.button1 = Button(self.button_frame, text="Hook", command=self.send_hook)
        self.button1.pack(side="left", padx=10)

        self.button2 = Button(self.button_frame, text="Unhook", command=self.send_unhook)
        self.button2.pack(side="left", padx=10)

        self.button3 = Button(self.button_frame, text="Print", command=self.send_print)
        self.button3.pack(side="left", padx=10)

        self.butDelete = Button(self.button_frame, text="Delete", command=self.clear_text)
        self.butDelete.pack(side="left", padx=10)

