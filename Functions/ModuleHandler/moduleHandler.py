from os import listdir, path, getcwd
import importlib
from types import ModuleType
import tkinter as tk
import tkinter.ttk as ttk

from Functions.ModuleHandler.failedModule import FailedModule
from Functions.ModuleHandler.activeModule import ActiveModule
from Functions.ModuleHandler.moduleAPI import API


class ModuleHandler:
    modules: ModuleType = []
    failed: list[FailedModule] = []
    active: list = []

    def __init__(self, api: API):
        self.api = api

        path1 = getcwd()  # getting path
        path1 += "\\Modules"
        folders = [item for item in listdir(path1) if path.isdir(path.join(path1, item))]

        for i in folders:
            file = path1 + "\\" + i
            if (module := self.load_module(file)) is not None:
                self.activate_module(module, file)

        if len(self.active) == 0:
            self.api.noModule.pack(anchor=tk.CENTER, expand=True)
            self.api.rightNotebook.pack_forget()

    def load_module(self, file: str):
        try:
            module = importlib.import_module(f"Modules.{path.basename(file)}.main")  # принцип: Modules/ModuleName/main.py
            self.modules.append(module)
            return module
        except ImportError as reason:
            self.failed.append(
                FailedModule(file, "Import error", reason)
            )
            return None

    def activate_module(self, module: ModuleType, file: str):
        try:
            active = module.Module(
                self.api
            )
        except Exception as reason:
            self.failed.append(
                FailedModule(file, "Activation error", reason)
            )
            return
        try:
            self.active.append(
                ActiveModule(
                    active.name,
                    active.version,
                    active.author,
                    active,
                    module
                )
            )
        except AttributeError as reason:
            self.failed.append(FailedModule(file, "Not enough information", reason))
