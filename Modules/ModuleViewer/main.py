"""
This module is used to handle module-related operations and see module information.
You can disable or enable modules.
"""
from Functions.ModuleHandler.activeModule import ActiveModule
from Functions.ModuleHandler.failedModule import FailedModule
from Functions.ModuleHandler.moduleAPI import API
import tkinter as tk

from UI.TKinter_addons.Tools.ScrollableFrame import ScrollableFrame
from Modules.ModuleViewer.leftModuleInfo import LeftSideInfo
from Modules.ModuleViewer.rightModuleInfo import RightModuleInfo


class Module:
    """
    This class represents a Module in the application. It handles module-related operations.

    Attributes:
    id_ (str): A unique identifier for the module.
    version (str): The version of the module.
    name (str): The name of the module.
    author (str): The author of the module.
    defaultNetworkAuth (bool): Indicates whether the module uses any network code.
    isUI (bool): Indicates whether the module changes a user interface.

    Methods:
    __init__(self, api: API): Initializes the Module object with the provided API instance.
    update_modules(self): Updates the list of found modules by iterating through the module startup order.
    """
    id_ = r"""KUKXsz0r4nmT<XHU6,u-dw\Iz<t^(ZbU='Q"H1Ot5{[6Klq9/W'nFo<u@7t0@-s#"""
    version = "0.1.0"
    name = "ModuleViewer"
    author = "ArT"
    defaultNetworkAuth = False
    isUI = True

    def __init__(self, api: API):
        self.api = api
        self.notebook = self.api.getRightNotebook()
        self.foundModules: list[ActiveModule | FailedModule] = []

        self.mainFrame = tk.Frame(api.getRightNotebook())
        self.mainFrame.pack(fill=tk.BOTH, expand=True)
        self.frame = tk.Frame(self.mainFrame)
        self.frame.pack(fill=tk.BOTH, expand=True)

        api.getRightNotebook().add(self.mainFrame, text="Module Viewer")

        self.warningLabel = tk.Label(self.mainFrame)
        self.warningLabel.pack(fill=tk.X, side=tk.BOTTOM)
        self.scrollableFrameList = ScrollableFrame(self.frame)

        self.scrollableFrameList.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollableFrameList.canvas.configure(width=200)
        self.scrollableFrameList.inner_frame.configure(bg='#B5B5B5')

        self.showModule = RightModuleInfo(self.frame, self.api.getDataManager(), self.id_, self.warningLabel)

        self.api.getRoot().after(10, self.update_modules)
        self.api.getRoot().after(500, self.update_modules)
        self.api.getRoot().after(1000, self.update_modules)
        self.api.getRoot().after(10000, self.update_modules)

    def update_modules(self):
        for module in self.api.getModuleHandler().moduleStartupOrder:
            if module in self.foundModules:  # if not already added to the list, add it now
                return
            self.foundModules.append(module)
            LeftSideInfo(
                self.scrollableFrameList.inner_frame,
                module,
                self.showModule,
            ).pack(pady=(0, 3), padx=1, fill=tk.X)
