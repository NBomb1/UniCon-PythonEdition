from Functions.ModuleHandler.moduleHandler import ModuleHandler
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.ModuleConnector.Server.ServerModuleConnectorManager import ModuleConnectorManager
from Functions.Network.ModuleConnector.Client.ModuleConnectorManager import ClientModuleConnectorManager


class ConnectorManager:
    server: ModuleConnectorManager = None
    client: ClientModuleConnectorManager = None

    def __init__(self, moduleHandler: ModuleHandler, accountManager: AccountManager):
        self.moduleHandler = moduleHandler
        self.accountManager = accountManager

    def setClient(self, messageTransfer: MessageTransfer):
        self.client = ClientModuleConnectorManager(messageTransfer, self.moduleHandler, self.accountManager)
        self.server = None

    def setServer(self):
        self.server = ModuleConnectorManager(self.accountManager)
        self.client = None
