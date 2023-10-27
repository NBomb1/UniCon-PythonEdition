from os import listdir, path, getcwd
import importlib
from types import ModuleType
import tkinter as tk

from Functions.ModuleHandler.failedModule import FailedModule
from Functions.ModuleHandler.activeModule import ActiveModule
from Functions.ModuleHandler.moduleAPI import API


class ModuleHandler:
    failed: list[FailedModule] = []
    active: list = []

    def __init__(self, api: API):
        try:
            self.api = api
            self.startModulesLoading()
        except Exception as error:
            self.showModuleLoaderError("Error:\n" + error.__str__())

    def startModulesLoading(self):
        path1 = getcwd()  # getting path
        path1 += "\\Modules"
        folders = [item for item in listdir(path1) if path.isdir(path.join(path1, item))]

        for i in folders:
            file = path1 + "\\" + i
            if (module := self.loadSingleModule(file)) is not None:
                self.activateSingleModule(module, file)

        if len(self.active) == 0:
            self.showModuleLoaderError("No modules found.")

    def loadSingleModule(self, file: str):
        load = f"Modules.{path.basename(file)}.main"  # path
        self.api.logs.sendLog(f"[ModuleHandler] Module {load} is loading.", 0)  # send log
        try:
            module = importlib.import_module(load)  # принцип: Modules/ModuleName/main.py  # loading module
            return module
        except ImportError as reason:
            self.failed.append(
                FailedModule(file, "Import error", reason)
            )
            self.api.logs.sendLog(f"[ModuleHandler] Couldn't load {load} module. {reason}", 0)
            return None

    def activateSingleModule(self, module: ModuleType, file: str):
        format_ = file.replace(getcwd(), '')
        try:
            self.api.logs.sendLog(f"[ModuleHandler] Module {format_} is initializing.", 0)  # send log
            active = module.Module(
                self.api
            )
            self.api.logs.sendLog(f"[ModuleHandler] Module {format_} initialized.", 0)  # send log
        except Exception as reason:
            self.failed.append(
                FailedModule(file, "Activation error", reason)
            )
            self.api.logs.sendLog(f"[ModuleHandler] Module {format_} has an internal error.", 0)
            return
        try:
            self.api.logs.sendLog(f"[ModuleHandler] Getting info from {format_}.", 0)  # send log
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
            self.api.logs.sendLog(f"[ModuleHandler] Couldn't get info from {format_}.", 0)  # send log
            self.failed.append(FailedModule(file, "Not enough information", reason))

    def showModuleLoaderError(self, message):
        self.api.rightNotebook.pack_forget()
        self.api.moduleLoaderError.configure(text=message)
        self.api.moduleLoaderError.pack(anchor=tk.CENTER)
