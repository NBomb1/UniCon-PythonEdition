import tkinter as tk
import tkinter.ttk as ttk
from inspect import stack
from os import getcwd

from Functions.ModuleHandler.moduleLoader import ModuleLoader
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.Network.TriggerManager import TriggerManager
from Functions.FileDataManager import FileDataManager
from Functions.logManager import Logs
from Functions.Exceptions.APIException import APIException
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from UI.MainMenu import MainMenu
    from Functions.Network.FileTransfer.FileTransfer import FileTransfer


class API:
    """
    API 1ST GENERATION
    """
    def __init__(self,
                 logs: Logs,
                 root: tk.Tk,
                 right_notebook: ttk.Notebook,
                 settings_notebook: ttk.Notebook,
                 mainMenu: 'MainMenu',
                 moduleLoaderError: tk.Label,
                 dataManager: FileDataManager,
                 triggerManager: TriggerManager,
                 connectorManager: ConnectorManager,
                 moduleLoader: ModuleLoader,
                 accountManager: AccountManager,
                 fileTransfer: 'FileTransfer'
                 ):
        self.__root = root
        self.__rightNotebook = right_notebook
        self.__settingsNotebook = settings_notebook
        self.__logs = logs
        self.__mainMenu = mainMenu
        self.__moduleLoaderError = moduleLoaderError
        self.__dataManager = dataManager
        self.__triggerManager = triggerManager
        self.__connectorManager = connectorManager
        self.__accountManager = accountManager
        self.__moduleLoader = moduleLoader
        self.__fileTransfer = fileTransfer

    def getRoot(self) -> tk.Tk:
        if self.__root is None:
            raise APIException.ObjectIsNull("Root is None")
        return self.__root

    def getRightNotebook(self) -> ttk.Notebook:
        if self.__rightNotebook is None:
            raise APIException.ObjectIsNull("RightNotebook is None")
        return self.__rightNotebook

    def getSettingsNotebook(self) -> ttk.Notebook:
        if self.__settingsNotebook is None:
            raise APIException.ObjectIsNull("SettingsNotebook is None")
        return self.__settingsNotebook

    def getLogs(self) -> Logs:
        if self.__logs is None:
            raise APIException.ObjectIsNull("Logs is None")
        return self.__logs

    def getMainMenu(self) -> 'MainMenu':
        if self.__mainMenu is None:
            raise APIException.ObjectIsNull("MainMenu is None")
        self.__logs.sendLog(f"[API] Accessed MainMenu from {stack()[1].filename.replace(getcwd(), '')}", 0)
        return self.__mainMenu

    def getModuleLoaderError(self) -> tk.Label:
        if self.__moduleLoaderError is None:
            raise APIException.ObjectIsNull("ModuleLoaderError is None")
        return self.__moduleLoaderError

    def getModuleLoader(self) -> ModuleLoader:
        if self.__moduleLoader is None:
            raise APIException.ObjectIsNull("ModuleLoader is None")
        return self.__moduleLoader

    def getDataManager(self) -> FileDataManager:
        if self.__dataManager is None:
            raise APIException.ObjectIsNull("DataManager is None")
        return self.__dataManager

    def getTriggerManager(self) -> TriggerManager:
        if self.__triggerManager is None:
            raise APIException.ObjectIsNull("TriggerManager is None")
        return self.__triggerManager

    def getConnectorManager(self) -> ConnectorManager:
        if self.__connectorManager is None:
            raise APIException.ObjectIsNull("ConnectorManager is None")
        return self.__connectorManager

    def getAccountManager(self) -> AccountManager:
        if self.__accountManager is None:
            raise APIException.ObjectIsNull("AccountManager is None")
        return self.__accountManager

    def getFileTransfer(self) -> 'FileTransfer':
        if self.__fileTransfer is None:
            raise APIException.ObjectIsNull("FileTransfer is None")
        return self.__fileTransfer
