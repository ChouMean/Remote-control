import tkinter as tk

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server")

        custom_font = ("Helvetica", 9)

        self.button1 = self.create_button("Start server", custom_font, self.start_server)
        self.button1.pack(padx=10, pady=10)

    def create_button(self, text, font, command):
        button = tk.Button(self.root, text=text, font=font, command=command, relief=tk.GROOVE)
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)
        return button

    def on_enter(self, event):
        event.widget.config(bg="#e6e6fa")

    def on_leave(self, event):
        event.widget.config(bg="SystemButtonFace")