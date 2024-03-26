from Functions.ModuleHandler.moduleAPI import API
from Functions.Tools.ScrollableFrame import ScrollableFrame
import tkinter as tk


class Module:
    version = "0.0.1"
    name = "Logs"
    author = "ArT"
    defaultNetworkAuth = False
    isOnlyUI = True

    def __init__(self, api: API):
        self.api = api
        self.notebook = self.api.getRightNotebook()

        self.frame = tk.Frame(self.api.getRightNotebook())

        self.notebook.add(self.frame, text='Accounts', state=tk.DISABLED)

        self.setup()

        self.notebook.tab(self.frame, state=tk.NORMAL)

    def setup(self):
        self.accountListFrame = ScrollableFrame(self.frame)

        self.accountListFrame.pack_propagate(False)

        self.accountInformationFrame = ScrollableFrame(self.frame)
        self.accountListFrame.pack(side=tk.LEFT, fill=tk.Y, ipadx=80)
        self.accountInformationFrame.pack(expand=True, fill=tk.BOTH)

        self.accountListFrame.inner_frame.configure(bg='yellow')
        self.accountInformationFrame.inner_frame.configure(bg='red')
