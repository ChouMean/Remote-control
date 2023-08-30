from StartDesigner import Start
from tkinter import messagebox
import threading

class StartFunc(Start):
    def __init__(self, nw, nr, ns):
        super().__init__()

        self.nw = nw
        self.nr = nr
        self.ns = ns

    def start_closing(self):
        self.destroy()

    def butStart_Click(self):
        self.nw.write("STARTID\n")
        self.nw.flush()
        thread = threading.Thread(target=self.start)
        thread.start()

    def start(self):
        self.nw.write(self.txtID.get() + "\n")
        self.nw.flush()
        s = self.nr.readline().strip()
        self.after(0, self.show_message_box, s)

    def show_message_box(self, message):
        messagebox.showinfo("Notification", message)