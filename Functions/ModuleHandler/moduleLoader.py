from os import listdir, path, getcwd
import importlib
from tkinter import ttk
from types import ModuleType
import tkinter as tk
from traceback import format_exc

from Functions.ModuleHandler.failedModule import FailedModule
from Functions.ModuleHandler.activeModule import ActiveModule
from Functions.FileDataManager import FileDataManager
from Functions.logManager import Logs
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Functions.ModuleHandler.moduleAPI import API
    from UI.MainMenu import MainMenu


class ModuleLoader:
    failed: list[FailedModule] = []
    active: list[ActiveModule] = []
    api: 'API' = None
    mainMenu: 'MainMenu' = None
    doNotLoadList: list[str] = []

    def __init__(self,
                 logs: Logs,
                 moduleLoaderError: tk.Label,
                 rightNotebook: ttk.Notebook,
                 root: tk.Tk,
                 fileDataManager: FileDataManager,
                 ):
        self.logs = logs
        self.moduleLoaderError = moduleLoaderError
        self.rightNotebook = rightNotebook
        self.root = root
        self.moduleStartupOrder: list[FailedModule | ActiveModule] = []
        self.fileDataManager = fileDataManager
        res = self.fileDataManager.get('main').get('doNotLoadList')
        self.doNotLoadList = res if res is not None else []

    def startLoading(self):
        self.logs.sendLog('[ModuleLoader] Loading external modules...', 0)
        try:
            self.mainMenu = self.api.getMainMenu()
            self.startModulesLoading()
        except Exception as error:
            self.showModuleLoaderError("Error:\n" + error.__str__() + '\n' + format_exc())
        self.logs.sendLog('[ModuleLoader] All modules were loaded successfully.', 0)

    def startModulesLoading(self):
        path1 = getcwd()  # getting path
        path1 += "\\Modules"
        folders = [item for item in listdir(path1) if path.isdir(path.join(path1, item))]

        for i in folders:
            file = path1 + "\\" + i
            if (module := self.loadSingleModule(file)) is not None:
                self.activateSingleModule(module, file)

        if len(list(filter(lambda x: not x.isDisabledManually, self.failed))) != 0:
            errorText = '\n'.join(map(lambda obj: obj.path, filter(lambda x: not x.isDisabledManually, self.failed)))
            self.showModuleLoaderError(f"Some modules ("
                                       f"{len(list(filter(lambda x: not x.isDisabledManually, self.failed)))}"
                                       f") have internal error.\n"
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
        self.logs.sendLog(f"[ModuleLoader] Module {load} is loading.", 0)  # send log
        try:
            module = importlib.import_module(load)  # принцип: Modules/ModuleName/main.py  # loading module
            return module
        except Exception as reason:
            module = FailedModule(file, "Import error", reason, format_exc())
            self.failed.append(module)
            self.moduleStartupOrder.append(module)
            self.logs.sendLog(f"[ModuleLoader] Couldn't import {load} module. {reason}", 0)
            return None

    def activateSingleModule(self, module: ModuleType, file: str, isInternal: bool = False):
        format_ = file.replace(getcwd(), '')
        active = None
        try:
            try:
                self.logs.sendLog(f"[ModuleLoader] Module {format_} is initializing.", 0)  # send log
                if module.Module.id_ in self.doNotLoadList:
                    self.logs.sendLog(f"[ModuleLoader] Module {format_} is in doNotLoadList.", 0)  # send log
                    module = FailedModule(file,
                                          "Module was disabled by user",
                                          Exception('No exception'),
                                          "No exception",
                                          True,
                                          module.Module.id_,
                                          )
                    self.failed.append(module)
                    self.moduleStartupOrder.append(module)
                    return
                active = module.Module(
                    self.api
                )
                if module.Module.id_ is None or len(module.Module.id_) != 64:
                    raise Exception("Id len must be equal 64")
                self.logs.sendLog(f"[ModuleLoader] Module {format_} initialized.", 0)  # send log
            except Exception as reason:
                module = FailedModule(file, "Activation error", reason, format_exc())
                self.failed.append(module)
                self.moduleStartupOrder.append(module)
                self.logs.sendLog(f"[ModuleLoader] Module {format_} has an internal error.", 0)
                return
            self.logs.sendLog(f"[ModuleLoader] Getting info from {format_}.", 0)  # send log
            module = ActiveModule(
                active.id_,
                active.name,
                active.version,
                active.author,
                active,
                module,
                active.defaultNetworkAuth,
                active.isUI,
                isInternal
            )
            self.active.append(module)
            self.moduleStartupOrder.append(module)
            self.logs.sendLog(f'[ModuleLoader] Module {active.name} has been loaded successfully', 0)
        except AttributeError as reason:
            self.logs.sendLog(f"[ModuleLoader] Couldn't get info from {format_}.", 0)  # send log
            module = FailedModule(file, "Not enough information", reason, format_exc())
            self.failed.append(module)
            self.moduleStartupOrder.append(module)
        return active

    def showModuleLoaderError(self, message):
        self.root.bell()
        self.mainMenu.left_button_create_server.configure(state=tk.DISABLED)
        self.mainMenu.left_button_connect.configure(state=tk.DISABLED)
        self.mainMenu.left_button_settings.configure(state=tk.DISABLED)
        self.rightNotebook.pack_forget()
        self.moduleLoaderError.configure(text=message)
        self.moduleLoaderError.pack(anchor=tk.CENTER)

    def hideModuleLoaderError(self):
        self.root.bell()
        self.mainMenu.left_button_create_server.configure(state=tk.NORMAL)
        self.mainMenu.left_button_connect.configure(state=tk.NORMAL)
        self.mainMenu.left_button_settings.configure(state=tk.NORMAL)
        self.moduleLoaderError.pack_forget()
        self.rightNotebook.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.NW, padx=(2, 0))

    def findById(self, id_: str) -> ActiveModule:
        for i in self.active:
            if i.id_ == id_:
                return i
