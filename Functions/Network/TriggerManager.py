from Functions.Network.Accounts.AccountAuthentication.Server.PreAuthAccount import PreAccount
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.MainChannel.Client.MainChannel import ClientMainChannel
from Functions.Network.MainChannel.Server.main import ServerMainChannel


class TriggerManager:
    serverStartedFunctions = []
    clientConnectedFunctions = []
    beforeAuthConnectionTrigger = []
    beforeAuthConnectionTrigger_Temporary = []

    def __init__(self, accountManager: AccountManager):
        """
        All functions, that adds TriggerFunction into list has word in the end "Trigger".
        All functions, that doesn't have this word, start all the functions in the list.
        """
        self.accountManager = accountManager

    def accountAddedTrigger(self, func: callable):
        self.accountManager.addNewAccountFunction(func)

    def accountAddedTriggerREMOVE(self, func: callable, ignoreException: bool = False):
        """Deletes trigger function if it exists."""
        try:
            self.accountManager.NewAccountTrigger.remove(func)
        except ValueError as e:
            if not ignoreException:
                raise e

    def accountRemovedTrigger(self, func: callable):
        self.accountManager.accountDisconnectedTrigger(func)

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

    def beforeAuthConnectionTemporaryTrigger(self, func: callable):
        self.beforeAuthConnectionTrigger_Temporary.append(func)

    def beforeAuthConnection(self, preAccount: PreAccount):
        for i in self.beforeAuthConnectionTrigger_Temporary:
            res = i(preAccount)
            if res or res is None:
                self.beforeAuthConnectionTrigger_Temporary.remove(i)
        for i in self.beforeAuthConnectionTrigger:
            i(preAccount)
        if preAccount.delete:
            preAccount.socket.close()
