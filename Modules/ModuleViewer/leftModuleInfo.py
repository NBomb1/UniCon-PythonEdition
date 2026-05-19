from Functions.ModuleHandler.activeModule import ActiveModule
from Functions.ModuleHandler.failedModule import FailedModule
import tkinter as tk

from Modules.ModuleViewer.rightModuleInfo import RightModuleInfo


class LeftSideInfo(tk.Frame):
    def __init__(
                self,
                root: tk.Widget,
                module: FailedModule | ActiveModule,
                rightWidgets: RightModuleInfo
            ):
        super().__init__(root)
        self.root = tk.Frame(self)
        self.root.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.rightWidgets = rightWidgets
        self.module = module

        self.statusFrame = tk.Frame(
            self.root,
            width=10,
            bg='red' if isinstance(module, FailedModule) else 'green'
        )
        self.statusFrame.pack(side=tk.LEFT, expand=False, fill=tk.Y, anchor=tk.W)

        self.labelModuleName = tk.Label(
            self.root,
            text=f"Mod: {module.name}" if isinstance(module, ActiveModule) else module.reason
        )
        self.labelModuleName.pack(anchor=tk.W, expand=True)

        if isinstance(module, ActiveModule):
            self.labelVersionModule = tk.Label(self.root, text=f"Ver: {module.version}")
            self.labelVersionModule.pack(anchor=tk.S + tk.W)
            self.labelVersionModule.bind("<Button-1>", self.on_click)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.statusFrame.bind("<Button-1>", self.on_click)
        self.labelModuleName.bind("<Button-1>", self.on_click)
        self.root.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        event.widget.config(cursor="hand2")

    def on_leave(self, event):
        event.widget.config(cursor="")

    def on_click(self, event):
        self.rightWidgets.showExactModuleInfo(self.module)
    #     self.updateFunc(self.account)
