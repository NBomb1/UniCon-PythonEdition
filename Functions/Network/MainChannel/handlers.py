import socket
import threading
from Functions.Server.PreAuthAccount import PreAccount
from Functions.Server.ServerAuthentication import Authentication
from Functions.Server.Account import Account
from Functions.Server.ServerPrefences import ServerInformation


class Handlers:
    isWorking = False

    def __init__(self, s: socket.socket, info: ServerInformation):
        self.socket = s
        self.server = info
        self._connectionFunctionTrigger = []
        self._NewAccountTrigger = []

    def handleIncomingConnections(self):
        self.isWorking = True

        def thread():
            while self.isWorking:
                try:
                    account = PreAccount(self.socket.accept())  # Creating Pre Account for others Modules
                    if not self.isWorking:  # checking if we still must accept connection
                        account.socket.close()  # closing connection if we shouldn't accept it
                        return  # stop working
                    for i in self._connectionFunctionTrigger:
                        i()  # getting all functions to call
                    Authentication.authentication(account, self.server, account.socket)
                except socket.timeout:
                    pass

        threading.Thread(target=thread).start()

    def RegisterConnectionHandler(self, function: callable):
        self._connectionFunctionTrigger.append(function)

    def RegisterNewAccountHandler(self, function: callable):
        self._connectionFunctionTrigger.append(function)

    def newAccount(self, account: Account):
        self.server.accountManager.add(account)

        for i in self._connectionFunctionTrigger:
            i()
