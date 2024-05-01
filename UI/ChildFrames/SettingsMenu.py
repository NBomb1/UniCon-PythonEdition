import tkinter as tk
from threading import Thread
from time import sleep

import settings
import tkinter.ttk as ttk

from Functions.Tools.DataSettings.FileDataManager import FileDataManager
from Functions.Tools.DataSettings.Widgets.IntegerEntry import IntegerEntry
from Functions.Tools.DataSettings.Widgets.NumberRange import NumberRange
from Functions.Tools.DataSettings.Widgets.StringEntry import StringEntry
from Functions.Tools.DataSettings.Widgets.checkWidget import CheckButton


class Settings(ttk.Notebook):
    portRange = None
    saveButton = None
    integerEntry = None
    stringEntry = None
    checkButton = None

    def __init__(self,
                 master: tk.Widget,
                 dataManager: FileDataManager,
                 nickname: StringEntry
                 ):
        self.nicknameWidget = nickname

        super().__init__(master)

        self.dataManager = dataManager

        self.settingsFrame = tk.Frame()

        self.fill_main()
        self.completeCheckButton()

    def fill_main(self):
        self.add(self.settingsFrame, text="Main Settings")
        self.checkButton = CheckButton(self.settingsFrame, 'Save nickname')
        self.integerEntry = IntegerEntry(self.settingsFrame, 'Integer')
        self.stringEntry = StringEntry(self.settingsFrame, 'String')

        # new one system in practical use
        self.portRange = NumberRange(
            self.settingsFrame,
            'Ports for use:',
            minFrom=settings.MainMenu.port_from,
            maxFrom=settings.MainMenu.port_to,
            minTo=settings.MainMenu.port_from,
            maxTo=settings.MainMenu.port_to,
            startNumberFrom=settings.MainMenu.port_from,
            startNumberTo=settings.MainMenu.port_to
        )
        self.portRange.connect(self.dataManager.get('main'), 'portRange')
        self.integerEntry.connect(self.dataManager.get('main'), 'integerTest')
        self.stringEntry.connect(self.dataManager.get('main'), 'stringTest')
        self.checkButton.connect(self.dataManager.get('main'), 'checkButton')

        self.checkButton.pack()
        self.portRange.pack()
        self.integerEntry.pack()
        self.stringEntry.pack()
        self.saveButton = tk.Button(self.settingsFrame, text='save', command=self.save)
        self.saveButton.pack()

    def save(self):
        self.disableSaving()
        self.portRange.save()
        self.integerEntry.save()
        self.stringEntry.save()
        self.checkButton.save()
        Thread(target=self.enableSaving, daemon=True).start()

    def enableSaving(self):
        sleep(settings.SettingsMenu.saveButtonWait)
        self.saveButton.configure(state=tk.NORMAL)

    def disableSaving(self):
        self.saveButton.configure(state=tk.DISABLED)

    def completeCheckButton(self):
        if self.checkButton.v.get():
            nickname = self.dataManager.get('main').get('nickname')
            if nickname != '':
                self.nicknameWidget.put(nickname)
