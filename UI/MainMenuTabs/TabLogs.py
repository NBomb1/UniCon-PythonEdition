import tkinter as tk
from UI.TKinter_addons.Text_chat import ChatText


class TabLogs(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Creating widgets
        self.text_logs = ChatText(self)
        self.button_save = tk.Button(self, text='Save')

        # Placing widgets
        self.text_logs.pack(fill=tk.BOTH)
        self.button_save.pack()
