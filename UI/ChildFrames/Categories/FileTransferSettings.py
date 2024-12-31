import tkinter as tk

from Functions.FileDataManager import FileDataManager
from UI.TKinter_addons.Tools.DataSettings.Widgets.checkWidget import CheckButton


class FileTransferSettings(tk.LabelFrame):

    def __init__(self, root: tk.Widget, dataManager: FileDataManager):
        super().__init__(
            root,
            text="FileTransfer Settings"
        )
        self.dataManager = dataManager

        self.checkButton_allowFileTransfer = CheckButton(self, 'Enable file transferring', True)
        self.checkButton_autoFileReceiving = CheckButton(self,
                                                         'Auto-accept file receiving (option will be available in '
                                                         'future updates)',
                                                         True
                                                         )
        self.checkButton_allowFileSendingFromUnknownModules_serverSide = \
            CheckButton(self, 'Allow file transferring from unknown '
                              'modules (server side)', False)
        self.checkButton_allowFileSendingFromUnknownModules = CheckButton(self, 'Allow file transferring from unknown '
                                                                                'modules', False)

        self.checkButton_allowFileTransfer.connect(self.dataManager.get('main'), 'allowFileSending')
        self.checkButton_allowFileSendingFromUnknownModules.connect(
            self.dataManager.get('main'),
            'allowFileReceivingFromUnknownModules'
        )
        self.checkButton_allowFileSendingFromUnknownModules_serverSide.connect(
            self.dataManager.get('main'),
            'allowFileReceivingFromUnknownModules_serverSide'
        )
        self.checkButton_autoFileReceiving.connect(self.dataManager.get('main'), 'autoFileReceiving')

        self.checkButton_allowFileTransfer.pack(anchor=tk.W)
        self.checkButton_allowFileSendingFromUnknownModules_serverSide.pack(anchor=tk.W)
        self.checkButton_allowFileSendingFromUnknownModules.pack(anchor=tk.W)
        self.checkButton_autoFileReceiving.pack(anchor=tk.W)
        self.checkButton_autoFileReceiving.configure(state=tk.DISABLED)
