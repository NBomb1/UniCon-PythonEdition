import tkinter as tk
from tkinter import ttk
from UI.TKinter_addons.Entry_Placeholder import EntryWithPlaceholder
from UI.TKinter_addons.Text_status import StatusText
from UI.MainMenuTabs.TabChat import TabChat
from UI.MainMenuTabs.TabParticipants import TabParticipants
from UI.MainMenuTabs.TabFiles import TabFiles
from UI.MainMenuTabs.TabLogs import TabLogs
from UI.SettingsMenu import Settings
from UI.window.WidnowCenter import center_main
from functools import partial
from threading import Thread
import settings


class MainMenu:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title('1C PROJECT - ' + settings.MainInfo.date)
        self.root.wm_minsize(900, 450)

        self.root.grid_columnconfigure(0, minsize=170)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self._left()
        self._right()
        center_main(self.root)

        self.root.mainloop()

    def _left(self):
        # Creating two frames that will contain all sorts of widgets
        self.left_frame1 = tk.Frame(self.root)

        # Creating widgets on the left frame
        self.left_text_status = StatusText(self.left_frame1)
        self.left_text_status.configure(wrap=tk.WORD, height=3, width=20)
        self.left_text_status.vbar.pack_forget()
        self.left_entry_ip = EntryWithPlaceholder(self.left_frame1, 'Type ip...')
        self.left_entry_nickname = EntryWithPlaceholder(self.left_frame1, 'Type your nickname...')
        self.left_label_port = tk.Label(self.left_frame1, text='Port channel: ')

        self.left_button_settings = tk.Button(self.left_frame1, text='Settings', command=partial(Settings, self.root))

        self.left_spinbox_port = tk.Spinbox(
            self.left_frame1,
            from_=settings.MainMenu.port_from,
            to=settings.MainMenu.port_to
        )

        # Placing widgets on the left frame
        self.left_text_status.pack(fill=tk.X, pady=(0, 10))
        self.left_entry_nickname.pack(fill=tk.X)
        self.left_entry_ip.pack(fill=tk.X)
        self.left_label_port.pack(fill=tk.X)
        self.left_spinbox_port.pack(fill=tk.X)
        self.left_button_settings.pack(side=tk.BOTTOM, ipadx=5)

        # Placing frames on the main screen
        self.left_frame1.pack(side=tk.LEFT, fill=tk.Y, anchor=tk.W)

    def _right(self):
        # Creating tab manager
        self.right_notebook = ttk.Notebook(self.root)

        # Creating tabs
        self.tab_chat = TabChat(self.right_notebook)
        self.tab_participants = TabParticipants(self.right_notebook)
        self.tab_files = TabFiles(self.right_notebook)
        self.tab_logs = TabLogs(self.right_notebook)

        # Adding tabs to tab manager
        self.right_notebook.add(self.tab_chat, text='Chat')
        self.right_notebook.add(self.tab_participants, text='Participants')
        self.right_notebook.add(self.tab_files, text='Files')
        self.right_notebook.add(self.tab_logs, text='Logs')

        # Placing tab manager
        self.right_notebook.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.NW, padx=5)
