import tkinter as tk
from tkinter import ttk

from Functions.logManager.logManager import Logs
from UI.TKinter_addons.Entry_Placeholder import EntryWithPlaceholder
from UI.TKinter_addons.Text_status import StatusText
from UI.MainMenuTabs.TabChat import TabChat
from UI.MainMenuTabs.TabParticipants import TabParticipants
from UI.MainMenuTabs.TabFiles import TabFiles
from UI.MainMenuTabs.TabLogs import TabLogs
from UI.ChildFrames.SettingsMenu import Settings
from UI.window.WidnowCenter import center_main
from Functions.ModuleHandler.moduleHandler import ModuleHandler
from Functions.ModuleHandler.moduleAPI import API
import settings


class MainMenu:
    def __init__(self, log: Logs):
        self.root = tk.Tk()
        self.root.wm_minsize(900, 450)
        self.changeTitle("MainMenu")

        # Main menu frame
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

        # Settings frame
        self.settingsFrame = Settings(self.mainFrame)

        self._left()
        self._right()

        self.module = ModuleHandler(
            API(
                log,
                self.root,
                self.right_notebook,
                self.settingsFrame,
                self.left_frame1,
                self.mainFrame,
                self.moduleLoaderError
            )
        )

        center_main(self.root)

        self.root.mainloop()

    def _left(self):
        # Creating two frames that will contain all sorts of widgets
        self.left_frame1 = tk.Frame(self.mainFrame)

        # Creating widgets on the left frame
        self.left_text_status = StatusText(self.left_frame1)
        self.left_text_status.configure(wrap=tk.WORD, height=3, width=20)
        self.left_entry_ip = EntryWithPlaceholder(self.left_frame1, 'Type ip...')
        self.left_entry_nickname = EntryWithPlaceholder(self.left_frame1, 'Type your nickname...')
        self.left_label_port = tk.Label(self.left_frame1, text='Port: ')

        self.left_button_connect = tk.Button(
            self.left_frame1,
            text='Connect to the server',
            width=20
        )
        self.left_button_create_server = tk.Button(
            self.left_frame1,
            text='Create the server',
            width=20
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

    def _right(self):
        # Creating tab manager
        self.right_notebook = ttk.Notebook(self.mainFrame)

        # Creating tabs
        self.tab_chat = TabChat(self.right_notebook)
        self.tab_participants = TabParticipants(self.right_notebook)
        self.tab_files = TabFiles(self.right_notebook)
        self.tab_logs = TabLogs(self.right_notebook)

        self.moduleLoaderError = tk.Label(self.mainFrame, text="No modules were loaded.", font=40)

        # Adding tabs to tab manager
        # self.right_notebook.add(self.tab_chat, text='Logs')
        # self.right_notebook.add(self.tab_participants, text='Participants')
        # self.right_notebook.add(self.tab_files, text='Files')
        # self.right_notebook.add(self.tab_logs, text='Logs')

        # Placing tab manager
        self.right_notebook.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.NW, padx=5)

    def changeTitle(self, name: str):
        self.root.title('1C PROJECT - ' + settings.MainInfo.date + " - " + name)

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
