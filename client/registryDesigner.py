import tkinter as tk
from tkinter import ttk

class RegistryEditor(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("registry")
        self.geometry("400x360")

        self.txtReg = tk.Text(self)
        self.txtReg.place(x=2, y=55, width=311, height=77)
        self.txtReg.insert(tk.END, "Contents")

        self.butSend = tk.Button(self, text="Send Content", command=self.button1_Click)
        self.butSend.place(x=319, y=55, width=75, height=77)

        self.butBro = tk.Button(self, text="Browser...", command=self.butBro_Click)
        self.butBro.place(x=319, y=20, width=75, height=23)

        self.txtBro = tk.Entry(self)
        self.txtBro.insert(0, "Link ...")
        self.txtBro.place(x=2, y=23, width=311, height=20)

        self.groupBox1 = ttk.LabelFrame(self, text="Change value")
        self.groupBox1.place(x=2, y=138, width=384, height=254)

        self.button1 = tk.Button(self.groupBox1, text="Send", command=self.send_value)
        self.button1.place(x=69, y=173, width=97, height=23)

        self.opApp = ttk.Combobox(self.groupBox1, values=["Get value", "Set value", "Delete value", "Create key", "Delete key"])
        self.opApp.set("Select function")
        self.opApp.place(x=6, y=19, width=372, height=21)
        self.opApp.bind("<<ComboboxSelected>>", self.update_fields)

        self.txtKQ = tk.Text(self.groupBox1)
        self.txtKQ.place(x=6, y=99, width=372, height=68)

        self.txtLink = tk.Entry(self.groupBox1)
        self.txtLink.insert(0, "Link")
        self.txtLink.place(x=6, y=46, width=372, height=20)

        self.txtValue = tk.Entry(self.groupBox1)
        self.txtValue.insert(0, "Value")
        self.txtValue.place(x=125, y=72, width=138, height=20)

        self.txtNameValue = tk.Entry(self.groupBox1)
        self.txtNameValue.insert(0, "Name value")
        self.txtNameValue.place(x=6, y=72, width=113, height=20)

        self.opTypeValue = ttk.Combobox(self.groupBox1, values=["String", "Binary", "DWORD", "QWORD", "Multi-String", "Expandable String"])
        self.opTypeValue.set("Data type")
        self.opTypeValue.place(x=269, y=72, width=109, height=21)

        self.butXoa = tk.Button(self.groupBox1, text="Delete", command=self.butXoa_Click)
        self.butXoa.place(x=192, y=173, width=94, height=23)

        self.protocol("WM_DELETE_WINDOW", self.registry_closing)