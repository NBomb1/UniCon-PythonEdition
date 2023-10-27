import tkinter as tk
import tkinter.ttk as ttk
from Functions.logManager.logManager import Logs


class API:
    def __init__(self,
                 logs: Logs,
                 root: tk.Tk,
                 right_notebook: ttk.Notebook,
                 settings_notebook: ttk.Notebook,
                 left_frame: tk.Frame,
                 main_frame: tk.Frame,
                 moduleLoaderError: tk.Label
                 ):
        self.root = root
        self.rightNotebook = right_notebook
        self.settingsNotebook = settings_notebook
        self.logs = logs
        self.leftFrame = left_frame
        self.mainFrame = main_frame
        self.moduleLoaderError = moduleLoaderError
