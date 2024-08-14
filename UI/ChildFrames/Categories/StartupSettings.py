from Functions.Network.SecurityInfo import SecurityInfo
import tkinter as tk

from Functions.Starting import TaskManager
from Functions.FileDataManager import FileDataManager
from UI.TKinter_addons.Tools.DataSettings.Widgets.StringEntry import StringEntry
from UI.TKinter_addons.Tools.DataSettings.Widgets.checkWidget import CheckButton


class StartUpSettings(tk.LabelFrame):
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

        self.checkButton_IKnowWhatIAmDoing = CheckButton(self,
                                                         'I know what I am doing',
                                                         False,
                                                         onClick=self.IKnowWhatIAmDoin_OnClick
                                                         )
        self.entry_startupDefaultArguments = StringEntry(self, 'Startup default arguments')
        if not TaskManager.isAdmin:
            self.checkButton_autoStart.configure(
                state=tk.DISABLED,
                text='Admin rights are required'
            )
        if TaskManager.disable:
            self.checkButton_autoStart.configure(
                state=tk.DISABLED,
                text="pywin32 is required"
            )

        self.checkButton_noAutoUpdateUserConfirmation.connect(
            self.dataManager.get('main'), 'checkButton_autoUpdateNoUserConfirmation'
        )
        self.checkButton_autoStart.connect(
            self.dataManager.get('main'), 'checkButton_autoStart'
        )
        self.checkButton_IKnowWhatIAmDoing.connect(
            self.dataManager.get('main'), 'checkButton_IKnowWhatIAmDoing'
        )
        self.entry_startupDefaultArguments.connect(
            self.dataManager.get('main'), 'entry_defaultArguments'
        )

        self.checkButton_noAutoUpdateUserConfirmation.pack(anchor=tk.W)
        self.checkButton_autoStart.pack(anchor=tk.W)

        self.checkButton_IKnowWhatIAmDoing.pack(anchor=tk.W)
        self.entry_startupDefaultArguments.pack(anchor=tk.W, fill=tk.X, padx=3)

        self.entry_startupDefaultArguments.configure(
            state=tk.DISABLED if not self.checkButton_IKnowWhatIAmDoing.v.get() else tk.NORMAL
        )

    def IKnowWhatIAmDoin_OnClick(self, *event):
        self.entry_startupDefaultArguments.configure(
            state=tk.NORMAL if
            not self.checkButton_IKnowWhatIAmDoing.v.get()  # value has not updated
            else tk.DISABLED
        )
