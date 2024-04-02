# the idea is to move buttons and their functions there for making readable code
import tkinter as tk
from tkinter import simpledialog, ttk

import settings
from Functions.Exceptions.Server import DataCollectionException
from Functions.ModuleHandler.moduleHandler import ModuleHandler
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Network.MainChannel.Client.MainChannel import ClientMainChannel
from Functions.Network.MainChannel.Server.main import ServerMainChannel
from Functions.Network.TriggerManager import TriggerManager
from Functions.Tools.logManager import Logs
from UI.ChildFrames.SettingsMenu import Settings
from UI.TKinter_addons.Entry_Placeholder import EntryWithPlaceholder


class MainMenuUIFunctions:
    # accountManager
    accountManager: AccountManager

    # triggerManager
    triggerManager: TriggerManager

    # window
    root: tk.Tk

    # Entry
    left_entry_nickname: EntryWithPlaceholder
    left_entry_ip: EntryWithPlaceholder

    # Settings
    settingsFrame: Settings

    # Button
    left_button_connect: tk.Button
    left_button_create_server: tk.Button
    left_button_settings: tk.Button

    # Spinbox
    left_spinbox_port: tk.Spinbox

    # Notebook
    right_notebook: ttk.Notebook

    # Label
    moduleLoaderError: tk.Label

    # Module Handler
    module: ModuleHandler

    # Logs manager
    logs: Logs

    server: ServerMainChannel
    client: ClientMainChannel

    def changeTitle(self, name: str):
        self.root.title('Unicon - ' + name + " - " + settings.MainInfo.startDate)

    def goSettings(self):
        self.settingsFrame.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.NW, padx=5)
        self.changeTitle("Settings")
        self.left_button_connect.pack_forget()
        self.left_button_create_server.pack_forget()
        self.left_button_settings.configure(
            text="Return",
            command=self.goMainFrame
        )
        if len(self.module.active):
            self.right_notebook.pack_forget()
        else:
            self.moduleLoaderError.pack_forget()

    def goMainFrame(self):
        self.settingsFrame.pack_forget()
        self.changeTitle("MainMenu")
        self.left_button_connect.pack(side=tk.BOTTOM, pady=(0, 5), padx=(5, 0))
        self.left_button_create_server.pack(side=tk.BOTTOM, pady=(0, 5), padx=(5, 0))
        self.left_button_settings.configure(
            text="Settings",
            command=self.goSettings
        )
        if len(self.module.active):
            self.right_notebook.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.NW, padx=5)
        else:
            self.moduleLoaderError.pack(anchor=tk.CENTER, expand=True)

    def startServer(self):
        try:
            # Getting data
            nickname = self.left_entry_nickname.get().lstrip(' ').rstrip(' ')
            ip = self.left_entry_ip.get()
            port = int(self.left_spinbox_port.get())

            # Checking correctness
            if len(nickname) < 3:
                raise DataCollectionException.UsernameException("No nickname was given.")
            if ip in ['', self.left_entry_ip.placeholder]:
                ip = '127.0.0.1'
                self.left_entry_ip.put('127.0.0.1')

            self.accountManager.setSelfAccount(SelfAccount(nickname))
            self.accountManager.getSelfAccount().tags.append('Owner')
            self.server = ServerMainChannel(self.logs, self.accountManager, ip, port, 3, None)
            self.left_entry_nickname.put(nickname)
            self.lockInteraction()
            self.triggerManager.serverStarted(self.server)
        except Exception as error:
            self.root.bell()
            self.logs.sendLog("Couldn't start the server. Reason: " + error.__str__(), -1)
            raise error

    def startClient(self):
        try:
            nickname = self.left_entry_nickname.get().lstrip(' ').rstrip(' ')
            ip = self.left_entry_ip.get()
            port = int(self.left_spinbox_port.get())

            if len(nickname) < 3:
                raise DataCollectionException.UsernameException("No nickname was given.")

            if ip in ['', self.left_entry_ip.placeholder]:
                ip = '127.0.0.1'
                self.left_entry_ip.put('127.0.0.1')

            self.accountManager.setSelfAccount(SelfAccount(nickname))

            self.client = ClientMainChannel(self.logs, self.accountManager, ip, port, self.askPassword, None)
            self.left_entry_nickname.put(nickname)
            self.lockInteraction()
            self.triggerManager.clientConnected(self.client)
        except Exception as error:
            self.root.bell()
            self.logs.sendLog("Couldn't connect to the server. Reason: " + error.__str__(), -1)
            raise error

    def askPassword(self) -> str:
        string = simpledialog.askstring("Ask String", "Wrong Password")
        return string

    def lockInteraction(self):
        self.left_entry_ip.configure(state=tk.DISABLED)
        self.left_entry_nickname.configure(state=tk.DISABLED)
        self.left_spinbox_port.configure(state=tk.DISABLED)
        self.left_button_create_server.configure(state=tk.DISABLED)
        self.left_button_connect.configure(state=tk.DISABLED)

    def unlockInteraction(self):
        self.left_entry_ip.configure(state=tk.NORMAL)
        self.left_entry_nickname.configure(state=tk.NORMAL)
        self.left_spinbox_port.configure(state=tk.NORMAL)
        self.left_button_create_server.configure(state=tk.NORMAL)
        self.left_button_connect.configure(state=tk.NORMAL)
