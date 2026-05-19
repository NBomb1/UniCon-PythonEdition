# the idea is to move buttons and their functions there for making readable code
import getpass
import tkinter as tk
from functools import partial
from os import getcwd
from subprocess import Popen
from sys import executable
from threading import Thread, Timer
from tkinter import simpledialog, ttk, messagebox

import settings
from Functions.Checks import checkInteger
from Functions.Exceptions.Server import DataCollectionException
from Functions.ModuleHandler.moduleAPI import API
from Functions.ModuleHandler.moduleLoader import ModuleLoader
from Functions.Network.Accounts.AccountAuthentication.Server.ServerAuthentication import Authentication
from Functions.Network.Accounts.AccountManager import AccountManager
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Network.FileTransfer.FileTransfer import FileTransfer
from Functions.Network.MainChannel.Client.MainChannel import ClientMainChannel
from Functions.Network.MainChannel.Server.main import ServerMainChannel
from Functions.Network.PingManager import PingManager
from Functions.Network.TriggerManager import TriggerManager
from Functions.Starting.UpdateChecker import UpdaterInfo
from Functions.Starting.UpdateChecker.checkVersion import check_for_updates
from Functions.logManager import Logs
from UI.ChildFrames.SettingsMenu import Settings
from UI.Info import Info
from UI.TKinter_addons.Tools.DataSettings.Widgets.StringEntry import StringEntry
from UI.TKinter_addons.confirmationForButtons import functionConfirmation


class MainMenuUIFunctions:
    new_version_available: bool = False
    # pingManager
    pingManager: PingManager.Module
    # fileTransfer: FileTransfer.FileTransfer

    # api
    api: API

    # FileTransfer
    fileTransfer: FileTransfer

    # Module Handler
    module: ModuleLoader

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
    left_spinbox_maxConnections: tk.Spinbox

    # variables
    maxConnections: tk.IntVar

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
    photoEnabledServer: tk.PhotoImage
    photoConnecting: tk.PhotoImage

    server: ServerMainChannel | None
    client: ClientMainChannel | None

    def changeTitle(self, name: str):
        self.root.title('UniCon - ' + name)

    def goSettings(self):
        self.settingsFrame.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.NW, padx=5)
        self.changeTitle("Settings")
        if self.new_version_available:
            self.left_button_connect.configure(text='Update application', command=self.update_app, state=tk.NORMAL)
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
            maxConns = self.maxConnections.get()

            # Checking correctness
            if maxConns < 0 or maxConns > 10000:
                raise ValueError("Incorrect maximum connections value.")
            if len(nickname) < 3 or len(nickname) > 15:
                nickname = getpass.getuser()
                self.left_entry_nickname.replace(nickname)
                self.logs.sendLog("[Warning] Nickname was changed to user's name because of its length.", -1)
            if len(nickname) < 3 or len(nickname) > 15:
                raise DataCollectionException.UsernameException("No nickname was given.")
            if password != '' and (len(password) < 3 or len(password) > 50):
                raise DataCollectionException.UsernameException("Password not in length range (from 3 to 50).")
            if ip in ['', self.left_entry_ip.placeholder]:
                ip = '127.0.0.1'
                self.left_entry_ip.replace('127.0.0.1')
            while '  ' in nickname:
                nickname = nickname.replace('  ', ' ')
            if nickname != self.left_entry_nickname.get():
                self.logs.sendLog("[Warning] The nickname was changed.", -1)
                self.left_entry_nickname.replace(nickname)

            self.accountManager.setSelfAccount(SelfAccount(nickname))
            self.accountManager.startedAsServer()
            self.accountManager.getSelfAccount().tags.append('Owner')
            self.accountManager.getSelfAccount().setId(Authentication.generate_random_id(8))

            self.server = ServerMainChannel(
                self.logs,
                self.accountManager,
                ip,
                port,
                maxConns,
                password if password else None,
                self.triggerManager.beforeAuthConnection,
                self.api.getConnectorManager(),
                self.settingsFrame.connectionSettings.checkButton_switchToIPv6.savedData,
                self.fileTransfer
            )
            self.left_entry_nickname.replace(nickname)
            self.lockInteraction()
            self.pingManager.getInfo(self.accountManager, True)
            self.triggerManager.serverStarted(self.server)
            self.left_status.configure(image=self.photoEnabledServer)
            self.root.wm_iconphoto(False, self.photoEnabledServer)
            self.left_status_label.configure(text='Server mode')
        except Exception as error:
            self.root.bell()
            self.logs.sendLog("Couldn't start the server. Reason: " + error.__str__(), -1)
            self.closeConnection()
            # self.accountManager.closeConnection()
            raise error

    def startClient(self, bell=True):
        def thread():
            try:
                print('Starting as client')
                nickname = self.left_entry_nickname.get().lstrip(' ').rstrip(' ')
                ip = self.left_entry_ip.get()
                port = int(self.left_spinbox_port.get())
                password = self.left_entry_password.get()

                while '  ' in nickname:
                    nickname = nickname.replace('  ', ' ')
                if len(nickname) < 3 or len(nickname) > 15:
                    nickname = getpass.getuser()
                    self.left_entry_nickname.replace(nickname)
                    self.logs.sendLog("[Warning] Nickname was changed to user's name because of its length.", -1)
                elif nickname != self.left_entry_nickname.get():
                    self.logs.sendLog("[Warning] Your nickname has been changed.", -1)
                    self.left_entry_nickname.replace(nickname)
                if len(nickname) < 3 or len(nickname) > 15:
                    raise DataCollectionException.UsernameException("No nickname was given.")
                if password != '' and (len(password) < 3 or len(password) > 50):
                    raise DataCollectionException.UsernameException("Password not in length range (from 3 to 50).")
                if ip in ['', self.left_entry_ip.placeholder]:
                    ip = '127.0.0.1'
                    self.left_entry_ip.replace('127.0.0.1')

                self.accountManager.setSelfAccount(SelfAccount(nickname))
                self.accountManager.startedAsClient()

                self.left_entry_nickname.replace(nickname)
                self.client = ClientMainChannel(
                    self.logs,
                    self.accountManager,
                    ip,
                    port,
                    self.api.getConnectorManager(),
                    self,
                    password if password else None,
                    self.settingsFrame.connectionSettings.checkButton_switchToIPv6.savedData
                )
                self.accountManager.selfAccountDisconnectedTrigger(self.selfClientDisconnected)
                self.triggerManager.clientConnected(self.client)
                self.pingManager.getInfo(self.accountManager, False)
                self.lockInteraction()
                self.left_status.configure(image=self.photoEnabledClient)
                self.root.wm_iconphoto(False, self.photoEnabledClient)
                self.left_status_label.configure(text='Client mode')
            except Exception as error:
                self.api.getAccountManager().selfAccountDisconnectedTriggerREMOVE(self.selfClientDisconnected, True)
                if bell:
                    self.root.bell()
                self.logs.sendLog("Couldn't connect to the server. Reason: " + error.__str__(), -1)
                self.logs.sendLog("Couldn't connect to the server. Reason: " + error.__str__(), 0)
                self.closeConnection()
                raise error

        Thread(target=thread, daemon=True).start()
        self.left_status.configure(image=self.photoConnecting)
        self.root.wm_iconphoto(False, self.photoConnecting)
        self.left_status_label.configure(text='Connecting...')
        self.lockInteraction(False)

    def askPassword(self) -> str:
        # _tkinter.TclError: window ".!_querystring" was deleted before its visibility changed
        temp = tk.Tk()
        temp.withdraw()
        string = simpledialog.askstring("Ask String", "Wrong Password", parent=temp)
        temp.destroy()
        return string

    def lockInteraction(self, unlockCloseConnection=True):
        self.left_entry_ip.configure(state=tk.DISABLED)
        self.left_entry_nickname.configure(state=tk.DISABLED)
        self.left_spinbox_port.configure(state=tk.DISABLED)
        self.left_spinbox_maxConnections.configure(
            state=tk.NORMAL if self.accountManager.getIsServer() else tk.DISABLED
        )
        self.left_button_create_server.configure(state=tk.DISABLED)
        self.left_button_connect.configure(state=tk.DISABLED)
        self.left_entry_password.configure(state=tk.DISABLED)
        if unlockCloseConnection:
            self.root.after(settings.MainMenu.switchModesDelay,
                            partial(
                                self.left_button_create_server.configure,
                                command=lambda: functionConfirmation(
                                    self.left_button_create_server,
                                    self.closeConnection,
                                    1, 3
                                ),
                                text='Close connection', state=tk.NORMAL)
                            )

    def unlockInteraction(self):
        self.left_entry_ip.configure(state=tk.NORMAL)
        self.left_entry_nickname.configure(state=tk.NORMAL)
        self.left_spinbox_port.configure(state=tk.NORMAL)
        self.left_spinbox_maxConnections.configure(state=tk.NORMAL)
        self.left_button_create_server.configure(state=tk.DISABLED)
        self.left_button_connect.configure(state=tk.DISABLED)
        self.left_entry_password.configure(state=tk.NORMAL)
        self.root.after(settings.MainMenu.switchModesDelay,
                        partial(
                            self.left_button_create_server.configure,
                            command=self.startServer,
                            text='Create the server',
                            state=tk.NORMAL
                        )
                        )
        self.root.after(
            settings.MainMenu.switchModesDelay,
            partial(self.left_button_connect.configure, state=tk.NORMAL)
        )

    def selfClientDisconnected(self, msg: dict):
        self.api.getAccountManager().selfAccountDisconnectedTriggerREMOVE(self.selfClientDisconnected)
        self.logs.sendLog(f'Got disconnected from server. Reason: {msg["reason"]}', -1)
        self.logs.sendLog(f'All info {msg}', -1)
        self.closeConnection()
        messagebox.showinfo(
            'Disconnected',
            f'You were kicked from server. Reason: \n{msg["reason"]}'
        )

    def closeConnection(self):
        if self.accountManager.getIsServer() is not None:
            self.accountManager.closeConnection()

    def connection_closed(self):
        self.server = None
        self.client = None
        if not self.accountManager.getIsServer():
            self.accountManager.selfAccountDisconnectedTriggerREMOVE(self.selfClientDisconnected, True)
        self.left_status.configure(image=self.photoDisabled)
        self.root.wm_iconphoto(False, self.photoDisabled)
        self.unlockInteraction()
        self.left_status_label.configure(text='No connection')

    def checkForUpdates(self, autoInstall=False):
        def thread():
            try:
                res = check_for_updates(
                    UpdaterInfo.URL,
                    UpdaterInfo.GITHUB_TOKEN,
                    Info.version,
                    UpdaterInfo.CLASS_NAME,
                    UpdaterInfo.ATTRIBUTE_NAME,
                    UpdaterInfo.REPO_OWNER,
                    UpdaterInfo.REPO_NAME,
                    UpdaterInfo.BRANCH,
                    UpdaterInfo.GITHUB_API_URL,
                    False
                )
            except Exception as e:
                self.logs.sendLog(f"An error occurred while checking updates: {e}", 0)
                return
            if res is None:
                self.logs.sendLog("[AutoUpdater] Couldn't check for updates.", 0)
                return
            if res.isOutdated:
                if autoInstall:
                    self.update_app(True)
                    return
                self.new_version_available = True
                if self.settingsFrame.winfo_ismapped():
                    self.goMainFrame()
                    self.goSettings()
                messagebox.showinfo(
                    "New update available!",
                    "New version available: " + res.newVersion + "\n" +
                    "You can go to settings and update your version.\n"
                    "ChangeLog: \n" + res.changelog
                )

        Thread(target=thread, daemon=True).start()

    def update_app(self, confirmed=False):
        if not confirmed and not messagebox.askyesno("Update", "Do you really want to update this application?\n"
                                                               "You might lose third party modules and your settings."):
            return
        self.logs.sendLog("Closing...", 0)
        try:
            Popen(
                [executable, getcwd() + "\\Functions\\Starting\\UpdateChecker\\UpdaterUI.py"],
                creationflags=0x00000008,
                close_fds=False,
                cwd=getcwd()
            )
            self.root.destroy()
            Timer(10, exit).start()
        except Exception as e:
            self.logs.sendLog("Error while starting update process.", 0)

    def autoReconnection(self, period=20):
        if (
                self.left_button_connect.cget('text') == 'Connect to the server'
                and
                self.left_button_connect.cget('state') == tk.NORMAL
        ):
            self.startClient(False)
        self.root.after(period * 1000, lambda: self.autoReconnection(period))

    def changeMaxConnections(self, *args):
        if self.accountManager.getIsServer():
            var = self.maxConnections.get()
            if checkInteger(var):
                self.accountManager.setMaxConnections(int(var))

    def showParticipants(self, event=None):
        # TODO: Finish it

        # l2.bind("<<B1-Enter>>", on_enter)
        # l2.bind("<<B1-Leave>>", on_leave)
        owner = self.accountManager.getOwner()
        if owner is not None:
            self.left_status_label.configure(
                text=f'{len(self.accountManager.getParticipants())}' +
                     (f'/{self.accountManager.getMaxConnections()}' if isinstance(owner, SelfAccount) else '') +
                     f' participant(s)'
            )
            # self.left_status.pack_forget()
            self.left_status_label.pack(anchor=tk.W)

    def hideParticipants(self, event=None):
        if self.left_entry_ip.cget('state') == tk.DISABLED:
            owner = self.accountManager.getOwner()
            if owner is None:
                self.left_status_label.configure(text='Connecting...')
            elif isinstance(owner, SelfAccount):
                self.left_status_label.configure(text='Server mode')
            else:
                self.left_status_label.configure(text='Client mode')
        else:
            self.left_status_label.configure(text='No connection')
        self.left_status_label.pack(anchor=tk.NW, side=tk.RIGHT, expand=True)
