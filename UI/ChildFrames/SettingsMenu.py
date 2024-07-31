import tkinter as tk
from threading import Thread
from time import sleep

import settings
import tkinter.ttk as ttk

from Functions.Tools.DataSettings.FileDataManager import FileDataManager
from UI.ChildFrames.Categories.ConnectionSettings import ConnectionSettings
from typing import TYPE_CHECKING


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

        super().__init__(master)

        self.dataManager = dataManager

        self.settingsFrame = tk.Frame()
        self.grid_rowconfigure(1, weight=1)

        self.fill_main()
        self.completeCheckButton()

    def fill_main(self):
        self.add(self.settingsFrame, text="Main Settings")
        self.settingsFrame.grid_rowconfigure(0, weight=1)
        self.settingsFrame.grid_columnconfigure(0, weight=1)

        self.connectionSettings = ConnectionSettings(self.settingsFrame, self.dataManager)

        self.saveButton = tk.Button(self.settingsFrame, text='save', command=self.save)

        self.connectionSettings.grid(row=0, column=0, sticky=tk.NSEW)
        self.saveButton.grid(row=1, columnspan=3, sticky=tk.NSEW)

    def save(self):
        self.disableSaving()

        self.connectionSettings.checkButton_saveNickname.save()
        self.connectionSettings.checkButton_savePassword.save()
        self.connectionSettings.checkButton_saveIP.save()
        self.connectionSettings.checkButton_savePort.save()

        Thread(target=self.enableSaving, daemon=True).start()

    def enableSaving(self):
        sleep(settings.SettingsMenu.saveButtonWait)
        self.saveButton.configure(state=tk.NORMAL)

    def disableSaving(self):
        self.saveButton.configure(state=tk.DISABLED)

    def completeCheckButton(self):
        if self.connectionSettings.checkButton_saveNickname.v.get():
            nickname = self.dataManager.get('main').get('nickname').__str__()
            if nickname:
                self.nicknameWidget.put(nickname)

        if self.connectionSettings.checkButton_saveIP.v.get():
            ip = self.dataManager.get('main').get('ip').__str__()
            if ip:
                self.ipWidget.put(ip)

        if self.connectionSettings.checkButton_savePassword.v.get():
            password = self.dataManager.get('main').get('password').__str__()
            if password:
                self.passwordWidget.put(password)

        if self.connectionSettings.checkButton_savePort.v.get():
            port = self.dataManager.get('main').get('port').__str__()
            if port:
                self.portWidget.set(port)
