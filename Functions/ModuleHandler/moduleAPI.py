import tkinter as tk
import tkinter.ttk as ttk

from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.Network.TriggerManager import TriggerManager
from Functions.Tools.DataSettings.FileDataManager import FileDataManager
from Functions.Tools.logManager import Logs
from Functions.Exceptions.APIException import APIException


class API:
    """
    API 1ST GENERATION
    """
    def __init__(self,
                 logs: Logs,
                 root: tk.Tk,
                 right_notebook: ttk.Notebook,
                 settings_notebook: ttk.Notebook,
                 left_frame: tk.Frame,
                 main_frame: tk.Frame,
                 moduleLoaderError: tk.Label,
                 dataManager: FileDataManager,
                 triggerManager: TriggerManager,
                 connectorManager: ConnectorManager
                 ):
        self.__root = root
        self.__rightNotebook = right_notebook
        self.__settingsNotebook = settings_notebook
        self.__logs = logs
        self.__leftFrame = left_frame
        self.__mainFrame = main_frame
        self.__moduleLoaderError = moduleLoaderError
        self.__dataManager = dataManager
        self.__triggerManager = triggerManager
        self.__connectorManager = connectorManager

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

    def getLeftFrame(self) -> tk.Frame:
        if self.__leftFrame is None:
            raise APIException.ObjectIsNull("LeftFrame is None")
        return self.__leftFrame

    def getMainFrame(self) -> tk.Frame:
        if self.__mainFrame is None:
            raise APIException.ObjectIsNull("MainFrame is None")
        return self.__mainFrame

    def getModuleLoaderError(self) -> tk.Label:
        if self.__moduleLoaderError is None:
            raise APIException.ObjectIsNull("ModuleLoaderError is None")
        return self.__moduleLoaderError

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
