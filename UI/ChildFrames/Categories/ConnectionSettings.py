from Functions.Network.SecurityInfo import SecurityInfo
import tkinter as tk

from Functions.Tools.DataSettings.FileDataManager import FileDataManager
from Functions.Tools.DataSettings.Widgets.IntegerEntry import IntegerEntry
from Functions.Tools.DataSettings.Widgets.checkWidget import CheckButton


class ConnectionSettings(tk.LabelFrame):
    ProgramDefaultPassword = SecurityInfo.defaultPassword
    MaxNumberOfConnections = 7

    def __init__(self, root: tk.Widget, dataManager: FileDataManager):
        super().__init__(
            root,
            text="Connection settings"
        )
        self.dataManager = dataManager
        self.root = root

        self.checkButton_savePassword = CheckButton(self, 'Save password', False)
        self.checkButton_saveIP = CheckButton(self, 'Save IP', False)
        self.checkButton_savePort = CheckButton(self, 'Save port', False)
        self.checkButton_saveNickname = CheckButton(self, 'Save nickname', True)

        self.checkButton_saveNickname.connect(self.dataManager.get('main'), 'checkButton_saveNickname')
        self.checkButton_savePassword.connect(self.dataManager.get('main'), 'checkButton_savePassword')
        self.checkButton_saveIP.connect(self.dataManager.get('main'), 'checkButton_saveIP')
        self.checkButton_savePort.connect(self.dataManager.get('main'), 'checkButton_savePort')

        self.checkButton_saveNickname.pack()
        self.checkButton_savePassword.pack()
        self.checkButton_saveIP.pack()
        self.checkButton_savePort.pack()
