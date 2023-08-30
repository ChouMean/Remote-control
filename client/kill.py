from killDesigner import KillApp
from tkinter import messagebox
import threading

class Kill(KillApp):
    def __init__(self, nw, nr, ns):
        super().__init__()
        self.nw = nw
        self.nr = nr
        self.ns = ns

    def butNhap_Click(self):
        self.nw.write("KILLID\n")
        self.nw.flush()
        thread = threading.Thread(target=self.kill)
        thread.start()

    def kill(self):
        self.nw.write(self.txtID.get() + "\n")
        self.nw.flush()
        s = self.nr.readline()
        messagebox.showinfo("Da diet", s)

    def kill_closing(self):
        self.destroy()