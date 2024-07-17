import os
import sys
import tkinter as tk
from os import getcwd
from tkinter import ttk

from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.MainChannel.Client.MainChannel import ClientMainChannel
from Functions.Network.MainChannel.Server.main import ServerMainChannel
from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.Network.PingManager import PingManager
from Functions.Network.TriggerManager import TriggerManager
from Functions.Tools.DataSettings.FileDataManager import FileDataManager
from Functions.Tools.DataSettings.Widgets.StringEntry import StringEntry
from Functions.Tools.logManager import Logs
from UI.MainMenuUIFunctions import MainMenuUIFunctions
from UI.ChildFrames.SettingsMenu import Settings
from UI.window.WindowCenter import center_main
from Functions.ModuleHandler.moduleHandler import ModuleHandler
from Functions.ModuleHandler.moduleAPI import API
import settings


class MainMenu(MainMenuUIFunctions):
    server: ServerMainChannel = None
    client: ClientMainChannel = None

    def __init__(self, log: Logs, dataManager: FileDataManager):
        self.absolutePath: str = "\\".join(os.path.abspath(str(sys.modules['__main__'].__file__)).split('\\')[:-1])
        self.logs = log
        self.root = tk.Tk()
        self.dataManager = dataManager
        self.accountManager = AccountManager(self.logs)
        # self.root = customtkinter.CTk()
        self.root.wm_minsize(925, 450)
        self.changeTitle("MainMenu")

        # Main menu frame
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)
        self.mainFrame.pack_propagate(False)  # not letting widgets expand self.root

        self._createLeftWidgets()
        self._createRightWidgets()

        # Settings frame
        self.settingsFrame = Settings(self.mainFrame, self.dataManager, self.left_entry_nickname)

        self.module = ModuleHandler(self.logs, self.moduleLoaderError, self.right_notebook, self.root)
        self.triggerManager = TriggerManager(self.accountManager)
        self.mcm = ConnectorManager(self.module, self.accountManager)

        self.api = API(
                log,
                self.root,
                self.right_notebook,
                self.settingsFrame,
                self.left_frame1,
                self.mainFrame,
                self.moduleLoaderError,
                self.dataManager,
                self.triggerManager,
                self.mcm,
                self.module,
                self.accountManager
            )
        self.module.api = self.api
        self.pingManager: PingManager.Module = self.module.activateSingleModule(
            PingManager,
            getcwd() + '\\Functions\\Network\\PingManager\\PingManager.py'
        )
        self.module.startLoading()

        center_main(self.root)

    def _createLeftWidgets(self):
        # Creating two frames that will contain all sorts of widgets
        self.left_frame1 = tk.Frame(self.mainFrame)

        # Creating widgets on the left frame
        # self.left_text_status = StatusText(self.left_frame1)
        # self.left_text_status.configure(wrap=tk.WORD, height=3, width=20)
        self.left_status_frame = tk.Frame(self.left_frame1)
        self.photoEnabledHost = tk.PhotoImage(file=self.absolutePath + r'\UI\Enabled-Host.gif')
        self.photoEnabledClient = tk.PhotoImage(file=self.absolutePath + r'\UI\Enabled-Client.gif')
        self.photoDisabled = tk.PhotoImage(file=self.absolutePath + r'\UI\Disabled.gif')

        self.photoDisabled = self.photoDisabled.subsample(3)
        self.photoEnabledClient = self.photoEnabledClient.subsample(3)
        self.photoEnabledHost = self.photoEnabledHost.subsample(3)

        self.root.wm_iconphoto(False, self.photoDisabled)

        self.left_status = tk.Label(
            self.left_status_frame,
            image=self.photoDisabled,
            width=self.photoDisabled.width(), height=self.photoDisabled.height()
        )
        self.left_status_label = tk.Label(self.left_status_frame, text='No connection', font=(None, 10))

        self.left_entry_ip = StringEntry(self.left_frame1, 'Type ip...')
        self.left_entry_nickname = StringEntry(self.left_frame1, 'Type your nickname...')
        # self.left_label_port = customtkinter.CTkLabel(self.left_frame1, text='Port: ')
        self.left_label_port = tk.Label(self.left_frame1, text='Port: ')

        self.left_button_connect = tk.Button(
            self.left_frame1,
            text='Connect to the server',
            width=20,
            command=self.startClient
        )
        self.left_button_create_server = tk.Button(
            self.left_frame1,
            text='Create the server',
            width=20,
            command=self.startServer
        )
        self.left_button_settings = tk.Button(
            self.left_frame1,
            text='Settings',
            command=self.goSettings,
            width=20
        )

        self.left_spinbox_port = tk.Spinbox(
            self.left_frame1,
            from_=settings.MainMenu.port_from,
            to=settings.MainMenu.port_to
        )

        # Placing widgets on the left frame
        # self.left_text_status.pack(fill=tk.X, pady=(5, 10), padx=(5, 0))
        self.left_status_frame.pack(fill=tk.X, pady=(5, 10), padx=(5, 0))
        self.left_status.pack(anchor=tk.E, side=tk.LEFT, expand=True)
        self.left_status_label.pack(anchor=tk.NW, side=tk.RIGHT, expand=True)
        self.left_entry_nickname.pack(fill=tk.X, padx=(5, 0))
        self.left_entry_ip.pack(fill=tk.X, padx=(5, 0))
        self.left_label_port.pack(fill=tk.X, padx=(5, 0))
        self.left_spinbox_port.pack(fill=tk.X, padx=(5, 0))
        self.left_button_settings.pack(side=tk.BOTTOM, pady=(0, 5), padx=(5, 0))
        self.left_button_connect.pack(side=tk.BOTTOM, pady=(0, 5), padx=(5, 0))
        self.left_button_create_server.pack(side=tk.BOTTOM, pady=(0, 5), padx=(5, 0))

        # Placing frames on the main screen
        self.left_frame1.pack(side=tk.LEFT, fill=tk.Y)

    def _createRightWidgets(self):
        # Creating tab manager
        self.right_notebook = ttk.Notebook(self.mainFrame)

        self.moduleLoaderError = tk.Label(self.mainFrame, text="No modules were loaded.", font=40)

        # Placing tab manager
        self.right_notebook.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.NW, padx=(2, 0))
