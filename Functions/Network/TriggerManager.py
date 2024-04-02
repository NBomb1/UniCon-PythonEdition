from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.MainChannel.Client.MainChannel import ClientMainChannel
from Functions.Network.MainChannel.Server.main import ServerMainChannel


class TriggerManager:
    serverStartedFunctions = []
    clientConnectedFunctions = []

    def __init__(self, accountManager: AccountManager):
        self.accountManager = accountManager

    def accountAddedTrigger(self, func: callable):
        self.accountManager.addNewAccountFunction(func)

    def serverStartedTrigger(self, func: callable):
        self.serverStartedFunctions.append(func)

    def serverStarted(self, serverInfo: ServerMainChannel):
        for func in self.serverStartedFunctions:
            func(serverInfo)

    def clientConnectedTrigger(self, func: callable):
        self.clientConnectedFunctions.append(func)

    def clientConnected(self, serverInfo: ClientMainChannel):
        for func in self.clientConnectedFunctions:
            func(serverInfo)
