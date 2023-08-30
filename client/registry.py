import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from registryDesigner import RegistryEditor

class Registry(RegistryEditor):
    def __init__(self, nw, nr, ns):
        super().__init__()

        self.nw = nw
        self.nr = nr
        self.ns = ns

    def butBro_Click(self):
        file_path = filedialog.askopenfilename(filetypes=[("Registry Files", "*.reg")])
        if file_path:
            self.txtBro.delete("0", "end")
            self.txtBro.insert("0", file_path)
            with open(file_path, "r") as file:
                try:
                    with open(file_path, "r", encoding="utf-16") as file:
                        registry_contents = file.read()
                        self.txtReg.delete("1.0", "end")
                        self.txtReg.insert("1.0", registry_contents)
                except Exception as e:
                    print("Error:", e)

    def update_fields(self, _):
        if self.opApp.get() == "Set value":
            self.txtNameValue.config(state="normal")
            self.txtValue.config(state="normal")
            self.opTypeValue.config(state="normal")
        else:
            self.txtNameValue.config(state="normal")
            self.txtValue.config(state="disabled")
            self.opTypeValue.config(state="disabled")

    def button1_Click(self):
        s = "REG"
        self.nw.write(s + "\n")
        self.nw.flush()

        s = self.txtReg.get("1.0", "end-1c")
        self.nw.write(s + "\n")
        self.nw.flush()

        s = self.nr.readline().strip()
        messagebox.showinfo("Response", s)

    def registry_closing(self):
        s = "QUIT"
        self.nw.write(s + "\n")
        self.nw.flush()
        self.destroy()

    def butXoa_Click(self):
        self.txt_kq.delete("1.0", "end")

    def send_value(self):
        try:
            s = "SEND"
            self.nw.write(s + '\n')
            self.nw.write(self.opApp.get() + '\n')
            self.nw.write(self.txtLink.get() + '\n')
            if(self.opApp.get() != "Create key" or self.opApp.get() != "Delete key"):
                self.nw.write(self.txtNameValue.get() + '\n')
            if(self.opApp.get() == "Set value"):
                self.nw.write(self.txtValue.get() + '\n')
                self.nw.write(self.opTypeValue.get() + '\n')
            self.nw.flush()
            response = self.nr.readline().strip()
            self.txtKQ.insert("end", response + "\n")
        except:
            self.txtKQ.insert("end", "Error" + "\n")