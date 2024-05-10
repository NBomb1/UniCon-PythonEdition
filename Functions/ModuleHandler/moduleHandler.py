from os import listdir, path, getcwd
import importlib
from tkinter import ttk
from types import ModuleType
import tkinter as tk
from traceback import format_exc

from Functions.ModuleHandler.failedModule import FailedModule
from Functions.ModuleHandler.activeModule import ActiveModule
from Functions.Tools.logManager import Logs


class ModuleHandler:
    failed: list[FailedModule] = []
    active: list[ActiveModule] = []
    api = None

    def __init__(self, logs: Logs, moduleLoaderError: tk.Label, rightNotebook: ttk.Notebook, root: tk.Tk):
        self.logs = logs
        self.moduleLoaderError = moduleLoaderError
        self.rightNotebook = rightNotebook
        self.root = root

    def startLoading(self):
        try:
            self.startModulesLoading()
        except Exception as error:
            self.showModuleLoaderError("Error:\n" + error.__str__() + '\n' + format_exc())

    def startModulesLoading(self):
        path1 = getcwd()  # getting path
        path1 += "\\Modules"
        folders = [item for item in listdir(path1) if path.isdir(path.join(path1, item))]

        for i in folders:
            file = path1 + "\\" + i
            if (module := self.loadSingleModule(file)) is not None:
                self.activateSingleModule(module, file)

        if len(self.failed) != 0:
            errorText = '\n'.join(map(lambda obj: obj.path, self.failed))
            self.showModuleLoaderError(f"Some modules ({len(self.failed)}) have internal error.\n"
                                       f"You can get info in a text file Modules Exception.txt\n"
                                       f"{errorText}"
                                       )
            self.root.after(6250, self.hideModuleLoaderError)
            for i in self.failed:
                with open(getcwd() + '\\Modules Exception.txt', 'w') as file:
                    text = f'Path: \n{i.path}\n\n' \
                           f'Reason: \n{i.reason}\n\n' \
                           f'CodeReason: \n{i.codeReason}\n\n' \
                           f'FormatExc: \n{i.format_exc}' + "\n" * 10
                    file.write(text)
        elif len(self.active) == 0:
            self.showModuleLoaderError("No modules found.")

    def loadSingleModule(self, file: str):
        load = f"Modules.{path.basename(file)}.main"  # path
        self.logs.sendLog(f"[ModuleHandler] Module {load} is loading.", 0)  # send log
        try:
            module = importlib.import_module(load)  # принцип: Modules/ModuleName/main.py  # loading module
            return module
        except ImportError as reason:
            self.failed.append(
                FailedModule(file, "Import error", reason, format_exc())
            )
            self.logs.sendLog(f"[ModuleHandler] Couldn't load {load} module. {reason}", 0)
            return None

    def activateSingleModule(self, module: ModuleType, file: str):
        format_ = file.replace(getcwd(), '')
        try:
            self.logs.sendLog(f"[ModuleHandler] Module {format_} is initializing.", 0)  # send log
            active = module.Module(
                self.api
            )
            if module.Module.id_ is None or len(module.Module.id_) != 64:
                raise Exception("Id must be equal 64")
            self.logs.sendLog(f"[ModuleHandler] Module {format_} initialized.", 0)  # send log
        except Exception as reason:
            self.failed.append(
                FailedModule(file, "Activation error", reason, format_exc())
            )
            self.logs.sendLog(f"[ModuleHandler] Module {format_} has an internal error.", 0)
            return
        try:
            self.logs.sendLog(f"[ModuleHandler] Getting info from {format_}.", 0)  # send log
            self.active.append(
                ActiveModule(
                    active.id_,
                    active.name,
                    active.version,
                    active.author,
                    active,
                    module,
                    active.defaultNetworkAuth,
                    active.isOnlyUI
                )
            )
        except AttributeError as reason:
            self.logs.sendLog(f"[ModuleHandler] Couldn't get info from {format_}.", 0)  # send log
            self.failed.append(FailedModule(file, "Not enough information", reason, format_exc()))
        return active

    def showModuleLoaderError(self, message):
        self.root.bell()
        self.rightNotebook.pack_forget()
        self.moduleLoaderError.configure(text=message)
        self.moduleLoaderError.pack(anchor=tk.CENTER)

    def hideModuleLoaderError(self):
        self.root.bell()
        self.moduleLoaderError.pack_forget()
        self.rightNotebook.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.NW, padx=(2, 0))

    def findById(self, id_: str) -> ActiveModule:
        for i in self.active:
            if i.id_ == id_:
                return i
