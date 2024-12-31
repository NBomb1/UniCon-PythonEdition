"""
Logs let you get information from different modules while program is running.
It can be used to track user actions, or log important events.
You can save information into the file.

Warning: It doesn't show information that was sent before module started.
"""
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
    version = "1.0.2"
    name = "Logs"
    author = "ArT"
    defaultNetworkAuth = False
    isUI = True

    font = (None, 11, "normal")
    currentId: int | str = -1
    limit_constant = 3_000_000  # limit for check
    idLog: dict[int | str, ChatText] = {}
    messageList: list[callable] = []

    def __init__(self, api: API):
        self.api = api
        self.api.getDataManager().create('Logs', getcwd() + '\\Modules\\Logs\\settings.yml')  # creates settings file

        self.storage = self.api.getDataManager().get("Logs")  # were all changes will be containing
        self._setupParameters()

        self.allIDs = [self.currentId]
        self.frame = tk.Frame(api.getRightNotebook())
        api.getRightNotebook().add(self.frame, text="Logs")

        self._create_widgets()
        self._place_widgets()
        self._configure_widgets()

        # Finishing it
        api.getLogs().registerHandler(
            int(self.currentId) if self.currentId.replace('-', '').isnumeric() else self.currentId,
            self.message
        )
        self.combobox_ids.set(self.currentId)
        self.message("This is the beginning of the logs.", self.currentId)

        self.handleMessages()

        # Registering ids which weren't found
        Thread(target=self.registerIDs, daemon=True).start()

    def message(self, message: str, id_: int, time: datetime = None):
        self.messageList.append(partial(self.message_, message, str(id_), time if time is not None else datetime.now()))

    def message_(self, message: str, id_: int, time: datetime):
        self.idLog[id_].create_message(
            {
                'message': message
            },
            time,
            '<{time}> {message}',
            {
                'message': 'system-message'
            }
        )

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
                while self.messageList:
                    self.messageList.pop(0)()
                sleep(0.01)
        Thread(target=loop, daemon=True).start()

    def clearButton(self):
        self.button_clear.configure(command=self.clearButtonConfirmation, text='Clear')
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

        self.message("[Logs] The logs have been saved. Path: " + filePath, 0)
        Thread(target=func, args=(filePath, copy)).start()

    def on_combobox_selected(self, event):
        currentId = self.combobox_ids.get()
        if currentId == self.currentId:
            return
        self.idLog[currentId].pack(fill=tk.BOTH, expand=True)
        self.idLog[str(self.currentId)].pack_forget()
        self.currentId = currentId
        self.storage.put('currentId', self.currentId)

    def registerIDs(self):
        for _ in range(0, 100):
            self.sortIds()
            for i in self.api.getLogs().registeredFunctions.keys():
                if str(i) not in self.allIDs:
                    self.allIDs.append(str(i))
                    self.idLog[str(i)] = ChatText(self.FrameChat)
                    self.sortIds()
                    self.api.getLogs().registerHandler(i, self.message)
                    self.idLog[str(i)].configure(wrap=tk.WORD, height=20, font=self.font)
                    self.message(f"[Logs] Log ID {i} has been found.", i)
            sleep(0.1)  # 10 secs of ids searching
        self.sortIds()

    def sortIds(self):
        temp = self.allIDs.copy()
        if 'All ids' in temp:
            temp.remove('All ids')
        temp = list(map(int, temp))
        temp.sort()
        temp.append('All ids')
        self.combobox_ids.configure(values=temp)

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
        if (a := self.storage.get('currentId')) is None:
            self.storage.put("currentId", self.currentId)
        else:
            self.currentId = a
