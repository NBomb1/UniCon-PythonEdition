import tkinter as tk
from threading import Thread
from time import sleep

import settings
import tkinter.ttk as ttk

from Functions.FileDataManager import FileDataManager
from UI.ChildFrames.Categories.ConnectionSettings import ConnectionSettings
from typing import TYPE_CHECKING

from UI.ChildFrames.Categories.PingManagerSettings import PingManagerSettings
from UI.ChildFrames.Categories.StartupSettings import StartUpSettings

if TYPE_CHECKING:
    from UI.MainMenu import MainMenu


class Settings(ttk.Notebook):
    saveButton = None

    def __init__(self,
                 master: tk.Widget,
                 dataManager: FileDataManager,
                 mainMenu: 'MainMenu'
                 ):
        self.nicknameWidget = mainMenu.left_entry_nickname
        self.ipWidget = mainMenu.left_entry_ip
        self.portWidget = mainMenu.variable_port
        self.passwordWidget = mainMenu.left_entry_password
        self.maxConnections = mainMenu.maxConnections

        super().__init__(master)

        self.dataManager = dataManager

        self.settingsFrame = tk.Frame()
        self.grid_rowconfigure(1, weight=1)

        self.fill_main()
        self.completeCheckButton()

    def fill_main(self):
        self.add(self.settingsFrame, text="Main Settings")
        self.settingsFrame.grid_rowconfigure(0, weight=1)
        # self.settingsFrame.grid_columnconfigure(0, weight=148)
        # self.settingsFrame.grid_columnconfigure(1, weight=110)
        # self.settingsFrame.grid_columnconfigure(2, weight=110)
        self.settingsFrame.grid_columnconfigure(0, weight=1)
        self.settingsFrame.grid_columnconfigure(1, weight=1)
        self.settingsFrame.grid_columnconfigure(2, weight=1)

        self.connectionSettings = ConnectionSettings(self.settingsFrame, self.dataManager)
        self.startupSettings = StartUpSettings(self.settingsFrame, self.dataManager)
        self.pingManagerSettings = PingManagerSettings(self.settingsFrame, self.dataManager)

        self.saveButton = tk.Button(self.settingsFrame, text='save', command=self.save)

        self.connectionSettings.grid(row=0, column=0, sticky=tk.NSEW)
        self.startupSettings.grid(row=0, column=1, sticky=tk.NSEW)
        self.pingManagerSettings.grid(row=0, column=2, sticky=tk.NSEW)

        self.saveButton.grid(row=1, columnspan=3, sticky=tk.NSEW)

    def save(self):
        self.disableSaving()

        # connection settings
        self.connectionSettings.checkButton_saveNickname.save()
        self.connectionSettings.checkButton_savePassword.save()
        self.connectionSettings.checkButton_saveIP.save()
        self.connectionSettings.checkButton_savePort.save()
        self.connectionSettings.checkButton_saveMaxConns.save()

        # startup settings
        self.startupSettings.checkButton_noAutoUpdateUserConfirmation.save()
        if self.startupSettings.checkButton_autoStart.cget('state') == tk.NORMAL:
            self.startupSettings.checkButton_autoStart.save()
        self.startupSettings.checkButton_IKnowWhatIAmDoing.save()
        self.startupSettings.entry_startupDefaultArguments.save()

        # ping manager settings
        self.pingManagerSettings.checkButton_sendFakeLatencyToServer.save()

        Thread(target=self.enableSaving, daemon=True).start()

    def enableSaving(self):
        sleep(settings.SettingsMenu.saveButtonWait)
        self.saveButton.configure(state=tk.NORMAL)

    def disableSaving(self):
        self.saveButton.configure(state=tk.DISABLED)

    def completeCheckButton(self):
        if self.connectionSettings.checkButton_saveNickname.savedData:
            nickname = self.dataManager.get('main').get('nickname')
            if nickname:
                self.nicknameWidget.put(nickname.__str__())

        if self.connectionSettings.checkButton_saveIP.savedData:
            ip = self.dataManager.get('main').get('ip')
            if ip:
                self.ipWidget.put(ip.__str__())

        if self.connectionSettings.checkButton_savePassword.savedData:
            password = self.dataManager.get('main').get('password')
            if password:
                self.passwordWidget.put(password.__str__())

        if self.connectionSettings.checkButton_savePort.savedData:
            port = self.dataManager.get('main').get('port')
            if port:
                self.portWidget.set(port.__str__())

        if self.connectionSettings.checkButton_saveMaxConns.savedData:
            maxConns = self.dataManager.get('main').get('maxConnections')
            if maxConns:
                self.maxConnections.set(maxConns.__str__())
