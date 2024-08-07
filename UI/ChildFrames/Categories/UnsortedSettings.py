from Functions.Network.SecurityInfo import SecurityInfo
import tkinter as tk

from Functions.Starting import TaskManager
from Functions.Tools.DataSettings.FileDataManager import FileDataManager
from Functions.Tools.DataSettings.Widgets.checkWidget import CheckButton


class UnsortedSettings(tk.LabelFrame):
    ProgramDefaultPassword = SecurityInfo.defaultPassword
    MaxNumberOfConnections = 7

    def __init__(self, root: tk.Widget, dataManager: FileDataManager):
        super().__init__(
            root,
            text="Startup settings"
        )
        self.dataManager = dataManager
        self.root = root

        self.checkButton_noAutoUpdateUserConfirmation = CheckButton(self, 'No auto-update confirmation', False)
        self.checkButton_autoStart = CheckButton(self, 'Auto startup', False, TaskManager.saveTaskSettings)
        if TaskManager.disable:
            self.checkButton_autoStart.configure(
                state=tk.DISABLED,
                text='Admin rights are required'
            )

        self.checkButton_noAutoUpdateUserConfirmation.connect(
            self.dataManager.get('main'), 'checkButton_autoUpdateNoUserConfirmation'
        )
        self.checkButton_autoStart.connect(
            self.dataManager.get('main'), 'checkButton_autoStart'
        )

        self.checkButton_noAutoUpdateUserConfirmation.pack()
        self.checkButton_autoStart.pack()
