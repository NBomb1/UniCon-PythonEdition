import tkinter as tk
from datetime import datetime
from threading import Thread
from time import sleep

from Functions.ModuleHandler.moduleAPI import API

from UI.TKinter_addons.Text_chat import ChatText


class Module:
    version = "0.0.1"
    name = "Logs"
    author = "ArT"

    def __init__(self, api: API):
        self.frame = tk.Frame(api.rightNotebook)
        self.limit_constant = 3_000_000
        self.limit = 0
        api.rightNotebook.add(self.frame, text="Logs")

        # Creating widgets
        self.text_logs = ChatText(self.frame)
        self.button_save = tk.Button(self.frame, text='Save')
        self.button_clear = tk.Button(self.frame, text='Clear', command=self.clearButtonConfirmation)

        # Placing widgets
        self.text_logs.pack(fill=tk.BOTH)
        self.button_save.pack(anchor=tk.NE, side=tk.LEFT, fill=tk.X, expand=True)
        self.button_clear.pack(anchor=tk.NW, side=tk.RIGHT, fill=tk.X, expand=True)
        self.text_logs.configure(wrap=tk.WORD, height=20)

        api.logs.registerHandler(0, self.message)
        self.message("All code has been done.", 0)

    def message(self, message: str, id_: int):
        if self.limit * 1.5 >= self.limit_constant:
            self.limit = 0
            self.text_logs.configure(state=tk.NORMAL)
            self.text_logs.delete("1.0", tk.END)
            self.text_logs.configure(state=tk.DISABLED)
            self.message("[Logs] All messages were forcefully cleared.", 0)
            # self.text_logs.bell()

        self.limit += self.text_logs.create_message(
            {
                'message': message
             },
            datetime.now(),
            '<ID=' + str(id_) + ' {time}> {message}',
            {
                'message': 'system-message'
            }
        )
        if self.limit >= self.limit_constant:
            pass

    def clearButtonConfirmation(self):
        def timer():
            sec = 0
            while sec != 9:
                if self.button_clear.cget("text") == 'Clear' and sec != 0:
                    return
                sec += 1

                if sec < 4:
                    self.button_clear.configure(text=f'Are you sure? {sec}...')
                    self.button_clear.configure(state=tk.DISABLED)
                elif sec > 8:
                    self.button_clear.configure(text='Clear', command=self.clearButtonConfirmation)
                elif sec >= 4:
                    self.button_clear.configure(text=f'Confirm {sec - 3}', state=tk.NORMAL, command=self.clearButton)
                sleep(1)

        Thread(target=timer, daemon=True).start()

    def clearButton(self):
        self.button_clear.configure(command=self.clearButtonConfirmation, text='Clear')
        self.limit = 0
        self.text_logs.configure(state=tk.NORMAL)
        self.text_logs.delete("1.0", tk.END)
        self.text_logs.configure(state=tk.DISABLED)
        self.message("[Logs] All messages were cleared by user.", 0)
