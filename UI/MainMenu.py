import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

import customtkinter

from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.Client.MainChannel import ClientMainChannel
from Functions.Network.Server.MainChannel.main import ServerMainChannel
from Functions.Tools.DataSettings.FileDataManager import DataManager
from Functions.Tools.logManager import Logs
from UI.MainMenuUIFunctions import MainMenuUIFunctions
from UI.TKinter_addons.Entry_Placeholder import EntryWithPlaceholder
from UI.TKinter_addons.Text_status import StatusText
from UI.ChildFrames.SettingsMenu import Settings
from UI.window.WindowCenter import center_main
from Functions.ModuleHandler.moduleHandler import ModuleHandler
from Functions.ModuleHandler.moduleAPI import API
import settings


class MainMenu(MainMenuUIFunctions):
    server: ServerMainChannel = None
    client: ClientMainChannel = None

    def __init__(self, log: Logs, dataManager: DataManager):
        self.logs = log
        self.root = tk.Tk()
        self.dataManager = dataManager
        self.accountManager = AccountManager()
        # self.root = customtkinter.CTk()
        self.root.wm_minsize(925, 450)
        self.changeTitle("MainMenu")

        # Main menu frame
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)
        self.mainFrame.pack_propagate(False)  # not letting widgets expand self.root

        # Settings frame
        self.settingsFrame = Settings(self.mainFrame, self.dataManager)

        self._createLeftWidgets()
        self._createRightWidgets()

        self.api = API(
                log,
                self.root,
                self.right_notebook,
                self.settingsFrame,
                self.left_frame1,
                self.mainFrame,
                self.moduleLoaderError,
                self.dataManager
            )
        self.module = ModuleHandler(self.api)

        center_main(self.root)
        self.root.mainloop()

    def _createLeftWidgets(self):
        # Creating two frames that will contain all sorts of widgets
        self.left_frame1 = tk.Frame(self.mainFrame)

        # Creating widgets on the left frame
        self.left_text_status = StatusText(self.left_frame1)
        self.left_text_status.configure(wrap=tk.WORD, height=3, width=20)
        self.left_entry_ip = EntryWithPlaceholder(self.left_frame1, 'Type ip...')
        self.left_entry_nickname = EntryWithPlaceholder(self.left_frame1, 'Type your nickname...')
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
        self.left_text_status.pack(fill=tk.X, pady=(5, 10), padx=(5, 0))
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
