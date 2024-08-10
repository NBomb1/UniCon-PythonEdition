from Functions.ModuleHandler.activeModule import ActiveModule
from Functions.ModuleHandler.failedModule import FailedModule
import tkinter as tk
from tkinter import messagebox

from Functions.FileDataManager import FileDataManager


class RightModuleInfo:
    def __init__(self,
                 root: tk.Widget,
                 dataManager: FileDataManager,
                 id_: str,
                 warningLabel: tk.Label):
        self.warningLabel = warningLabel
        res = dataManager.get('main').get('doNotLoadList')
        res = res if res is not None else list()
        dataManager.get('main').put('doNotLoadList', res)
        self.notToLoadModules: list[str] = res
        self.dataManager = dataManager
        self.id_ = id_

        self.root = root

        self.moduleName = tk.Label(self.root, justify=tk.LEFT)
        self.moduleId = tk.Label(self.root, justify=tk.LEFT)
        self.version = tk.Label(self.root, justify=tk.LEFT)
        self.author = tk.Label(self.root, justify=tk.LEFT)
        self.defaultNetworkAuth = tk.Label(self.root, justify=tk.LEFT)
        self.isUI = tk.Label(self.root, justify=tk.LEFT)
        self.isInternal = tk.Label(self.root, justify=tk.LEFT)
        self.description = tk.Label(self.root, justify=tk.LEFT)
        # self.description = ScrolledText(self.root, wrap=tk.WORD, font=(None, 9), state=tk.DISABLED)
        self.disableButton = tk.Button(self.root)

    def showActiveInfo(self):
        self.moduleName.pack(anchor=tk.W)
        self.moduleId.pack(anchor=tk.W)
        self.version.pack(anchor=tk.W)
        self.author.pack(anchor=tk.W)
        self.defaultNetworkAuth.pack(anchor=tk.W)
        self.isUI.pack(anchor=tk.W)
        self.isInternal.pack(anchor=tk.W)
        self.description.pack(anchor=tk.W)  # , fill=tk.BOTH, expand=True)
        self.disableButton.pack(anchor=tk.W, fill=tk.X)

    def showFailedInfo(self):
        self.moduleName.pack(anchor=tk.W)
        self.moduleId.pack(anchor=tk.W)
        self.version.pack(anchor=tk.W)
        self.author.pack(anchor=tk.W)
        self.disableButton.pack(anchor=tk.W, fill=tk.X)

    def hide_all(self):
        self.moduleName.pack_forget()
        self.moduleId.pack_forget()
        self.version.pack_forget()
        self.author.pack_forget()
        self.defaultNetworkAuth.pack_forget()
        self.isUI.pack_forget()
        self.isInternal.pack_forget()
        self.disableButton.pack_forget()
        self.description.pack_forget()
        # self.description.config(state=tk.NORMAL)
        # self.description.delete('1.0', tk.END)

    def showExactModuleInfo(self, module: ActiveModule | FailedModule):
        if isinstance(module, ActiveModule):
            self.hide_all()
            self.showActiveInfo()
            self.moduleName.config(text=f"Module name: {module.name}")
            self.moduleId.config(text=f"Module ID: {module.id_}")
            self.version.config(text=f"Version: {module.version}")
            self.author.config(text=f"Author: {module.author}")
            self.defaultNetworkAuth.config(text=f"Using Network: {module.defaultNetworkAuth}")
            self.isUI.config(text=f"Changes UI: {module.isUI}")
            self.isInternal.config(text=f"Is internal module: {module.isInternal}")
            self.disableButton.config(text=f"Disable" if module.id_ not in self.notToLoadModules else "Enable",
                                      command=lambda: self.disable(module)
                                      if module.id_ not in self.notToLoadModules
                                      else self.enable(module),
                                      state=tk.DISABLED if module.isInternal else tk.NORMAL
                                      )
            self.description.configure(text=f"Description: "
                                            f"{None if module.description is None else module.description.rstrip()}"
                                       )
            # self.description.config(state=tk.DISABLED)
        else:
            self.hide_all()
            self.moduleName.config(text=f"Module path: {module.path}")
            self.moduleId.config(text=f"Reason: {module.reason}")
            self.version.config(text=f'CodeReason: {module.codeReason}')
            self.author.config(text=f'FormatExc: \n{module.format_exc}')
            self.disableButton.config(text=f"Disable" if module.id_ not in self.notToLoadModules else "Enable",
                                      command=lambda: self.disable(module)
                                      if module.id_ not in self.notToLoadModules
                                      else self.enable(module),
                                      state=tk.DISABLED if not module.isDisabledManually else tk.NORMAL
                                      )
            self.showFailedInfo()

    def disable(self, module: ActiveModule | FailedModule):
        if (
                module.id_ == self.id_ and not
        messagebox.askyesno(
            "Warning",
            "Important Notice: \n"
            "Disabling this module will result in the loss of functionality "
            "for controlling other modules. "
            "You will need to manually activate "
            "this module at the next program startup.\n\n"
            "Continue?"
        )
        ):
            return

        if isinstance(module, ActiveModule):
            self.notToLoadModules.append(module.id_)
            self.disableButton.config(text="Enable", command=lambda: self.enable(module))
        else:
            self.notToLoadModules.append(module.id_)
            self.disableButton.config(text="Enable", command=lambda: self.enable(module))
        self.warningLabel.config(
            text="Warning: Changes will apply after restart.",
            fg="red",
            bg='yellow'
        )

    def enable(self, module: ActiveModule | FailedModule):
        if isinstance(module, ActiveModule):
            self.notToLoadModules.remove(module.id_)
            self.disableButton.config(text="Disable", command=lambda: self.disable(module))
        else:
            self.notToLoadModules.remove(module.id_)
            self.disableButton.config(text="Disable", command=lambda: self.disable(module))
        self.warningLabel.config(
            text="Warning: Changes will apply after restart.",
            fg="red",
            bg='yellow'
        )
