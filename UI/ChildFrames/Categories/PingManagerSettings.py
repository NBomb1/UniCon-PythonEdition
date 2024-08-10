import tkinter as tk

from Functions.FileDataManager import FileDataManager
from UI.TKinter_addons.Tools.DataSettings.Widgets.checkWidget import CheckButton


class PingManagerSettings(tk.LabelFrame):

    def __init__(self, root: tk.Widget, dataManager: FileDataManager):
        super().__init__(
            root,
            text="PingManager Settings"
        )
        self.dataManager = dataManager

        self.checkButton_sendFakeLatencyToServer = CheckButton(self, 'Add random latency', False)

        self.checkButton_sendFakeLatencyToServer.connect(self.dataManager.get('main'), 'sendFakeLatency')

        self.checkButton_sendFakeLatencyToServer.pack(anchor=tk.W)

