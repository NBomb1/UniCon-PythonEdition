import tkinter as tk
from datetime import datetime
from functools import partial
from os import getcwd
from threading import Thread
from time import sleep
from tkinter import filedialog, ttk

from Functions.ModuleHandler.moduleAPI import API

from UI.TKinter_addons.Text_chat import ChatText


class Module:
    id_ = 'v1tsW@Joi3z^+98K[p7DhMRX4f6Ngx9p]EFC=|x0h5L]uQoSXwGM%6Zefi[cd1bu'
    version = "0.0.1"
    name = "Logs"
    author = "ArT"
    defaultNetworkAuth = False
    isOnlyUI = True

    font = (None, 11, "normal")
    currentId: int = -1
    limit_constant = 3_000_000  # limit for check
    limit = 0  # current number
    idLog: dict[int, ChatText] = {}
    messageList: list[callable] = []

    def __init__(self, api: API):
        self.api = api
        self._setupParameters()

        self.allIDs = [self.currentId]
        self.frame = tk.Frame(api.getRightNotebook())

        api.getRightNotebook().add(self.frame, text="Logs")

        self._create_widgets()
        self._place_widgets()
        self._configure_widgets()

        # Finishing it
        api.getLogs().registerHandler(self.currentId, self.message)
        self.combobox_ids.set(self.currentId)
        self.message("This is starting text logs.", self.currentId)

        self.handleMessages()

        # Registering ids which weren't found
        Thread(target=self.registerIDs, daemon=True).start()

    def message(self, message: str, id_: int):
        self.messageList.append(partial(self.message_, message, id_))

    def message_(self, message: str, id_: int):
        if self.limit * 1.5 >= self.limit_constant:
            self.limit = 0
            self.idLog[id_].configure(state=tk.NORMAL)
            self.idLog[id_].delete("1.0", tk.END)
            self.idLog[id_].configure(state=tk.DISABLED)
            self.message("[Logs] All messages were forcefully cleared.", id_)

        self.limit += self.idLog[id_].create_message(
            {
                'message': message
            },
            datetime.now(),
            '<{time}> {message}',
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
                    self.button_clear.configure(text=f'Confirm {sec - 3}...', state=tk.NORMAL, command=self.clearButton)
                sleep(1)

        Thread(target=timer, daemon=True).start()

    def handleMessages(self):
        def loop():
            while True:
                for func in self.messageList:
                    func()
                    self.messageList.remove(func)
                sleep(0.001)
        Thread(target=loop, daemon=True).start()

    def clearButton(self):
        self.button_clear.configure(command=self.clearButtonConfirmation, text='Clear')
        self.limit = 0
        self.idLog[self.currentId].configure(state=tk.NORMAL)
        self.idLog[self.currentId].delete("1.0", tk.END)
        self.idLog[self.currentId].configure(state=tk.DISABLED)
        self.message("[Logs] All messages were cleared by user.", self.currentId)

    def saveLogs(self):
        copy = self.idLog[self.currentId].get("1.0", tk.END)
        filePath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"Logs id {self.currentId}",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Logs As"
        )
        if not filePath:
            return

        def func(path, logs):
            with open(path, mode='w', encoding='utf-8') as file:
                file.write(logs)

        self.message("[Logs] Logs has been saved. Path: " + filePath, 0)
        Thread(target=func, args=(filePath, copy)).start()

    def on_combobox_selected(self, event):
        currentId = int(self.combobox_ids.get())
        if currentId == self.currentId:
            return
        self.idLog[currentId].pack(fill=tk.BOTH, expand=True)
        self.idLog[self.currentId].pack_forget()
        self.currentId = currentId

    def registerIDs(self):
        for _ in range(0, 100):
            sleep(0.0001)
            for i in self.api.getLogs().registeredFunctions.keys():
                if i not in self.allIDs:
                    self.allIDs.append(i)
                    self.idLog[i] = ChatText(self.FrameChat)
                    self.allIDs.sort()
                    self.combobox_ids.configure(values=self.allIDs)
                    self.api.getLogs().registerHandler(i, self.message)
                    self.idLog[i].configure(wrap=tk.WORD, height=20, font=self.font)
                    self.message(f"[Logs] ID {i} have been found.", i)

    def _create_widgets(self):
        # Creating widgets
        self.text_logs = ChatText(self.frame)

        self.FrameChat = tk.Frame(self.frame)  # top
        self.FrameButton = tk.Frame(self.frame)   # mid
        self.FrameCombobox = tk.Frame(self.frame)  # low

        self.idLog[self.currentId] = ChatText(self.FrameChat)
        self.idLog[self.currentId].configure(wrap=tk.WORD, height=20, font=self.font, undo=False)

        self.button_save = tk.Button(self.FrameButton, text='Save', command=self.saveLogs, width=1)
        self.button_clear = tk.Button(self.FrameButton, text='Clear', command=self.clearButtonConfirmation, width=1)
        self.combobox_label = tk.Label(self.FrameCombobox, text='Logs ID')
        self.combobox_ids = ttk.Combobox(self.FrameCombobox, state='r')

    def _place_widgets(self):
        # Placing widgets
        self.combobox_label.pack()
        self.combobox_ids.pack(side=tk.LEFT, anchor=tk.N, expand=True)

        # Placing main frames
        self.FrameChat.pack(fill=tk.BOTH, expand=True)
        self.FrameButton.pack(fill=tk.X)
        self.FrameCombobox.pack(fill=tk.X, pady=(0, 3))

        # Each log id has text widget
        self.idLog[self.currentId].pack(fill=tk.BOTH, expand=True)

        # Log buttons
        self.button_save.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.button_clear.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _configure_widgets(self):
        self.text_logs.configure(wrap=tk.WORD, height=20)
        self.combobox_ids.bind("<<ComboboxSelected>>", self.on_combobox_selected)

    def _setupParameters(self):
        self.api.getDataManager().create('Logs', getcwd() + '\\Modules\\Logs\\settings.yml')
        if (a := self.api.getDataManager().get("Logs").get('currentId')) is None:
            self.api.getDataManager().get("Logs").put("currentId", self.currentId)
        else:
            self.currentId = a
