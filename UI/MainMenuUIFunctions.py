# the idea is to move buttons and their functions there for making readable code
import tkinter as tk
import traceback
from functools import partial
from os import getcwd
from threading import Thread
from tkinter import simpledialog, ttk, messagebox

import settings
from Functions.Exceptions.Server import DataCollectionException
from Functions.ModuleHandler.moduleAPI import API
from Functions.ModuleHandler.moduleHandler import ModuleHandler
from Functions.Network.Accounts.AccountAuthentication.Server.ServerAuthentication import Authentication
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Network.MainChannel.Client.MainChannel import ClientMainChannel
from Functions.Network.MainChannel.Server.main import ServerMainChannel
from Functions.Network.PingManager import PingManager
from Functions.Network.TriggerManager import TriggerManager
from Functions.Starting.UpdateChecker import UpdaterInfo
from Functions.Starting.UpdateChecker.Processes import run_independent_process
from Functions.Starting.UpdateChecker.checkVersion import check_for_updates
from Functions.Tools.DataSettings.Widgets.StringEntry import StringEntry
from Functions.Tools.logManager import Logs
from UI.ChildFrames.SettingsMenu import Settings
from UI.Info import Info


class MainMenuUIFunctions:
    new_version_available: bool = False
    # pingManager
    pingManager: PingManager.Module

    # api
    api: API

    # Module Handler
    module: ModuleHandler

    # accountManager
    accountManager: AccountManager

    # triggerManager
    triggerManager: TriggerManager

    # window
    root: tk.Tk

    # Entry
    left_entry_nickname: StringEntry
    left_entry_ip: StringEntry
    left_entry_password: StringEntry

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
    left_status_label: tk.Label
    left_status: tk.Label

    # Logs manager
    logs: Logs

    # Photos
    photoDisabled: tk.PhotoImage
    photoEnabledClient: tk.PhotoImage
    photoEnabledHost: tk.PhotoImage

    server: ServerMainChannel | None
    client: ClientMainChannel | None

    def changeTitle(self, name: str):
        self.root.title('Unicon - ' + name + " - " + settings.MainInfo.startDate)

    def goSettings(self):
        self.settingsFrame.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.NW, padx=5)
        self.changeTitle("Settings")
        if self.new_version_available:
            self.left_button_connect.configure(text='Update application', command=self.update_app)
        else:
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
        if self.new_version_available:
            self.left_button_connect.configure(text='Connect to the server', command=self.startClient)
        else:
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
            print('Starting as server')
            # Getting data
            nickname = self.left_entry_nickname.get().lstrip(' ').rstrip(' ')
            ip = self.left_entry_ip.get()
            port = int(self.left_spinbox_port.get())
            password = self.left_entry_password.get()

            # Checking correctness
            if len(nickname) < 3 or len(nickname) > 15:
                raise DataCollectionException.UsernameException("No nickname was given.")
            if password != '' and (len(password) < 3 or len(password) > 50):
                raise DataCollectionException.UsernameException("Password not in length range (from 3 to 50).")
            if ip in ['', self.left_entry_ip.placeholder]:
                ip = '127.0.0.1'
                self.left_entry_ip.put('127.0.0.1')

            self.accountManager.setSelfAccount(SelfAccount(nickname))
            self.accountManager.startedAsServer()
            self.accountManager.getSelfAccount().tags.append('Owner')
            self.accountManager.getSelfAccount().setId(Authentication.generate_random_id(8))

            self.server = ServerMainChannel(
                self.logs,
                self.accountManager,
                ip,
                port,
                50,
                password if password else None,
                self.triggerManager.beforeAuthConnection,
                self.api.getConnectorManager()
            )
            self.left_entry_nickname.put(nickname)
            self.lockInteraction()
            self.triggerManager.serverStarted(self.server)
            self.pingManager.getInfo(self.accountManager, True)
            self.left_status.configure(image=self.photoEnabledHost)
            self.root.wm_iconphoto(False, self.photoEnabledHost)
            self.left_status_label.configure(text='Host mode')
        except Exception as error:
            self.root.bell()
            self.logs.sendLog("Couldn't start the server. Reason: " + error.__str__(), -1)
            self.closeConnection()
            # self.accountManager.closeConnection()
            raise error

    def startClient(self):
        try:
            print('Starting as client')
            nickname = self.left_entry_nickname.get().lstrip(' ').rstrip(' ')
            ip = self.left_entry_ip.get()
            port = int(self.left_spinbox_port.get())
            password = self.left_entry_password.get()

            if len(nickname) < 3 or len(nickname) > 15:
                raise DataCollectionException.UsernameException("No nickname was given.")
            if password != '' and (len(password) < 3 or len(password) > 50):
                raise DataCollectionException.UsernameException("Password not in length range (from 3 to 50).")

            if ip in ['', self.left_entry_ip.placeholder]:
                ip = '127.0.0.1'
                self.left_entry_ip.put('127.0.0.1')

            self.accountManager.setSelfAccount(SelfAccount(nickname))
            self.accountManager.startedAsClient()

            self.left_entry_nickname.put(nickname)
            self.client = ClientMainChannel(
                self.logs,
                self.accountManager,
                ip,
                port,
                self.api.getConnectorManager(),
                self.askPassword,
                password if password else None,
            )
            # self.client.messageTransfer.registerFunction('close', self.accountManager.disconnectedFromServer)
            self.accountManager.selfAccountDisconnectedTrigger(self.selfClientDisconnected)
            self.triggerManager.clientConnected(self.client)
            self.pingManager.getInfo(self.accountManager, False)
            self.lockInteraction()
            self.left_status.configure(image=self.photoEnabledClient)
            self.root.wm_iconphoto(False, self.photoEnabledClient)
            self.left_status_label.configure(text='Client mode')
        except Exception as error:
            self.root.bell()
            self.logs.sendLog("Couldn't connect to the server. Reason: " + error.__str__(), -1)
            self.logs.sendLog("Couldn't connect to the server. Reason: " + error.__str__(), 0)
            # self.accountManager.closeConnection()
            self.closeConnection()
            traceback.format_exc()
            raise error

    def askPassword(self) -> str:
        string = simpledialog.askstring("Ask String", "Wrong Password")
        return string

    def lockInteraction(self):
        self.left_entry_ip.configure(state=tk.DISABLED)
        self.left_entry_nickname.configure(state=tk.DISABLED)
        self.left_spinbox_port.configure(state=tk.DISABLED)
        # self.left_button_create_server.configure(state=tk.DISABLED)
        self.left_button_create_server.configure(state=tk.DISABLED)
        self.left_button_connect.configure(state=tk.DISABLED)
        self.left_entry_password.configure(state=tk.DISABLED)
        self.root.after(500,
                        partial(
                            self.left_button_create_server.configure, command=self.closeConnection,
                            text='Close connection', state=tk.NORMAL)
                        )

    def unlockInteraction(self):
        self.left_entry_ip.configure(state=tk.NORMAL)
        self.left_entry_nickname.configure(state=tk.NORMAL)
        self.left_spinbox_port.configure(state=tk.NORMAL)
        # self.left_button_create_server.configure(state=tk.NORMAL)
        self.left_button_create_server.configure(state=tk.DISABLED)
        self.left_button_connect.configure(state=tk.DISABLED)
        self.left_entry_password.configure(state=tk.NORMAL)
        self.root.after(500,
                        partial(
                            self.left_button_create_server.configure,
                            command=self.startServer,
                            text='Create the server',
                            state=tk.NORMAL
                        )
                        )
        self.root.after(500, partial(self.left_button_connect.configure, state=tk.NORMAL))

    def selfClientDisconnected(self, msg: dict):
        self.api.getAccountManager().SelfDisconnectTrigger.remove(self.selfClientDisconnected)
        self.logs.sendLog(f'Got disconnected from server. Reason: {msg["reason"]}', -1)
        self.logs.sendLog(f'All info {msg}', -1)
        # self.unlockInteraction()
        self.closeConnection()
        messagebox.showinfo(
            'Disconnected',
            f'You were kicked from server. Reason: \n{msg["reason"]}'
        )

    def closeConnection(self):
        if self.accountManager.getIsServer():
            self.accountManager.closeConnection()
            self.server = None
        elif not self.accountManager.getIsServer():
            self.accountManager.closeConnection()
            self.client = None
        self.left_status.configure(image=self.photoDisabled)
        self.root.wm_iconphoto(False, self.photoDisabled)
        self.unlockInteraction()
        self.left_status_label.configure(text='No connection')

    def checkForUpdates(self):
        def thread():
            res = check_for_updates(
                UpdaterInfo.URL,
                UpdaterInfo.GITHUB_TOKEN,
                Info.version,
                UpdaterInfo.CLASS_NAME,
                UpdaterInfo.ATTRIBUTE_NAME
            )
            if res.isOutdated:
                self.new_version_available = True
                messagebox.showinfo(
                    "New update available!",
                    "New version available: " + res.newVersion + "\n" +
                    "You can go to settings and update your version.\n"
                    "ChangeLog: " + res.changelog
                )

        Thread(target=thread).start()

    def update_app(self):
        if not messagebox.askyesno("Update", "Do you really want to update this application?\n"
                                             "You might lose third party modules and your settings."):
            return
        self.logs.sendLog("Closing...", 0)
        try:
            run_independent_process(
                getcwd() + "\\Functions\\Starting\\UpdateChecker\\UpdaterUI.py"
            )
            self.root.after(1000, self.root.destroy)
        except Exception as e:
            self.logs.sendLog("Error while starting update process.", 0)
