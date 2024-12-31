from Functions.Network.SecurityInfo import SecurityInfo
import tkinter as tk

from Functions.Starting import TaskManager
from Functions.FileDataManager import FileDataManager
from UI.TKinter_addons.Tools.DataSettings.Widgets.StringEntry import StringEntry
from UI.TKinter_addons.Tools.DataSettings.Widgets.checkWidget import CheckButton


class StartUpSettings(tk.LabelFrame):
    def __init__(self, root: tk.Widget, dataManager: FileDataManager):
        super().__init__(
            root,
            text="Startup settings"
        )
        self.dataManager = dataManager
        self.root = root

        # Creating widgets
        self.checkButton_noAutoUpdateUserConfirmation = CheckButton(self, 'No auto-update confirmation', False)
        self.checkButton_autoStart = CheckButton(self,
                                                 'Auto startup',
                                                 False,
                                                 lambda x: (
                                                     TaskManager.saveTaskSettings(
                                                         self.checkButton_autoStart_ApplyForThisUser,
                                                         x
                                                     )
                                                 ),
                                                 onClick=self.checkButton_autoStart_OnClick
                                                 )
        self.checkButton_autoStart_ApplyForThisUser = CheckButton(self,
                                                                  'Apply for this user',
                                                                  True,
                                                                  )

        self.checkButton_IKnowWhatIAmDoing = CheckButton(self,
                                                         'I know what I am doing',
                                                         False,
                                                         onClick=self.IKnowWhatIAmDoin_OnClick
                                                         )
        self.entry_startupDefaultArguments = StringEntry(self, 'Startup default arguments', minLen=0, maxLen=5000)
        # linking buttons to its files
        self.checkButton_noAutoUpdateUserConfirmation.connect(
            self.dataManager.get('main'), 'checkButton_autoUpdateNoUserConfirmation'
        )
        self.checkButton_autoStart.connect(
            self.dataManager.get('main'), 'checkButton_autoStart'
        )
        self.checkButton_autoStart_ApplyForThisUser.connect(
            self.dataManager.get('main'), 'checkButton_autoStart_ApplyForThisUser'
        )
        self.checkButton_IKnowWhatIAmDoing.connect(
            self.dataManager.get('main'), 'checkButton_IKnowWhatIAmDoing'
        )
        self.entry_startupDefaultArguments.connect(
            self.dataManager.get('main'), 'entry_defaultArguments'
        )

        # conditions for auto-startup
        self.autoStartState = tk.NORMAL
        self.autoStartText = None
        if TaskManager.disable:
            self.autoStartState = tk.DISABLED
            self.autoStartText = "pywin32 is required"
        elif not TaskManager.isAdmin:
            self.autoStartState = tk.DISABLED
            self.autoStartText = "Admin rights are required"

        self.checkButton_autoStart.configure(state=self.autoStartState, text=self.autoStartText)
        self.checkButton_autoStart_ApplyForThisUser.configure(state=self.autoStartState, text=self.autoStartText)

        self.checkButton_autoStart_ApplyForThisUser.configure(state=tk.NORMAL
                                                              if (
                self.checkButton_autoStart.v.get() and self.autoStartState == tk.NORMAL
        )
                                                              else tk.DISABLED
                                                              )

        # packing widgets
        self.checkButton_noAutoUpdateUserConfirmation.pack(anchor=tk.W)
        self.checkButton_autoStart.pack(anchor=tk.W)
        self.checkButton_autoStart_ApplyForThisUser.pack(anchor=tk.W, padx=(20, 0))

        self.checkButton_IKnowWhatIAmDoing.pack(anchor=tk.W)
        self.entry_startupDefaultArguments.pack(anchor=tk.W, fill=tk.X, padx=3)

        self.entry_startupDefaultArguments.configure(
            state=tk.DISABLED if not self.checkButton_IKnowWhatIAmDoing.v.get() else tk.NORMAL
        )

    def IKnowWhatIAmDoin_OnClick(self, *event):
        self.entry_startupDefaultArguments.configure(
            state=tk.DISABLED if
            not self.checkButton_IKnowWhatIAmDoing.v.get()  # value has not updated
            else tk.NORMAL
        )
        # self.entry_startupDefaultArguments.configure(
        #     state=tk.NORMAL if
        #     not self.checkButton_IKnowWhatIAmDoing.v.get()  # value has not updated
        #     else tk.DISABLED
        # )

    def checkButton_autoStart_OnClick(self, *event):
        self.checkButton_autoStart_ApplyForThisUser.configure(
            state=tk.NORMAL if
            not self.checkButton_autoStart.v.get() and self.autoStartState == tk.NORMAL  # value has not updated yet
            else tk.DISABLED
        )
