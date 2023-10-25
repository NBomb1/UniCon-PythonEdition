import tkinter as tk
import tkinter.ttk as ttk
from Functions.ModuleHandler.moduleAPI import API

from UI.TKinter_addons.Text_chat import ChatText


class Module:
    version = "0.0.1"
    name = "Logs"
    author = "ArT"

    def __init__(self, api: API):
        self.frame = tk.Frame(api.rightNotebook)
        api.rightNotebook.add(self.frame, text="Logs")

        # Creating widgets
        self.text_logs = ChatText(self.frame)
        self.button_save = tk.Button(self.frame, text='Save')

        # Placing widgets
        self.text_logs.pack(fill=tk.BOTH)
        self.button_save.pack()
        api.logs.registerHandler(0, self.message)

    def message(self, *args):
        print(args)
