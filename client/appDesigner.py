import tkinter as tk
from tkinter import ttk, font
import threading

class ApplicationList(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Process Viewer")
        self.geometry("365x250")
        
        self.configure(bg="white")
        
        self.header_frame = ttk.Frame(self)
        self.header_frame.pack(pady=2)

        self.button1 = ttk.Button(self, text="Kill", command=self.button2_Click)
        self.button1.place(x=24, y=12, width=76, height=47)

        self.button2 = ttk.Button(self, text="List", command=self.button1_Click)
        self.button2.place(x=106, y=12, width=69, height=47)

        self.button3 = ttk.Button(self, text="Start", command=self.button3_Click)
        self.button3.place(x=261, y=12, width=69, height=47)

        self.listView1 = ttk.Treeview(self, columns=("Name Process", "ID Process", "Count Thread"), show="headings")
        columns = [("Name Process", "Name Process"), ("ID Process", "ID Process"), ("Count Thread", "Thread")]
        for col_name, col_text in columns:
            self.listView1.heading(col_name, text=col_text)
            self.listView1.column(col_name, width=font.Font().measure(col_text))
            if col_name != "Name Process":
                self.listView1.column(col_name, anchor="center")
        self.listView1.place(x=24, y=74, width=320, height=162)

        self.button4 = ttk.Button(self, text="Clear", command=self.button4_Click)
        self.button4.place(x=181, y=12, width=74, height=47)

        self.protocol("WM_DELETE_WINDOW", self.listApp_closing)

        self.scrollbar = ttk.Scrollbar(self.listView1, orient="vertical", command=self.listView1.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listView1.configure(yscrollcommand=self.scrollbar.set)
        
        self.protocol("WM_DELETE_WINDOW", self.listApp_closing)

   
    def sort_name(self, column):
        if hasattr(self, "sorting_thread") and self.sorting_thread.is_alive():
            return

        self.sorting_thread = threading.Thread(target=self.perform_sorting, args=(column,))
        self.sorting_thread.start()

    def perform_sorting(self, column):
        with threading.Lock():
            self.sort_order = "asc" if not hasattr(self, "sort_order") else self.sort_order
            items = self.listView1.get_children("")
            
            column_index = self.get_column_index(column)

            items = sorted(items, key=lambda item: self.listView1.item(item, "values")[column_index], reverse=self.sort_order == "desc")
            
            for item in items:
                self.listView1.move(item, "", "end")
            
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
    
    def get_column_index(self, column_name):
        column_ids = self.listView1["columns"]
        return column_ids.index(column_name)