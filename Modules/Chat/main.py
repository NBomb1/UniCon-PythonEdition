import tkinter as tk
import tkinter.ttk as ttk

from UI.TKinter_addons.Text_chat import ChatText


class Module:
    def __init__(self, window: tk.Tk, notebook: ttk.Notebook):
        self.frame = tk.Frame(notebook)
        notebook.add(self.frame, text="Logs")

        # Creating widgets
        self.text_logs = ChatText(self.frame)
        self.button_save = tk.Button(self.frame, text='Save')

        # Placing widgets
        self.text_logs.pack(fill=tk.BOTH)
        self.button_save.pack()


