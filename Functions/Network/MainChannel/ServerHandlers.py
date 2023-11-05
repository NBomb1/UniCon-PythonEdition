import socket
import threading

from Functions.Server.AccountManager import AccountManager
from Functions.Server.PreAuthAccount import PreAccount
from Functions.Server.ServerAuthentication import Authentication
from Functions.Server.Account import Account
from Functions.logManager.logManager import Logs


class ServerInformation:
    def __init__(self, ip: str, port: int, password: str, s: socket.socket):  # , handler):
        self.ip = ip
        self.port = port
        self.accountManager = AccountManager()
        self.password = password
        self.modules = []
        self.handler = Handlers(s, self)


class Handlers:
    isWorking = False

    def __init__(self, s: socket.socket, info: ServerInformation):
        self.socket = s
        self.server = info
        self._connectionFunctionTrigger = []
        self._NewAccountTrigger = []

    def handleIncomingConnections(self, logs: Logs):
        self.isWorking = True

        def thread():
            while self.isWorking:
                try:
                    logs.sendLog("[MainChannel] Waiting for new connections. ", -1)
                    account = PreAccount(self.socket.accept())  # Creating Pre Account for others Modules
                    if not self.isWorking:  # checking if we still must accept connection
                        account.socket.close()  # closing connection if we shouldn't accept it
                        return  # stop working
                    logs.sendLog(f"[MainChannel] Got new connection! {account.ip}:{account.port}", -1)
                    for i in self._connectionFunctionTrigger:
                        i()  # getting all functions to call
                    logs.sendLog("[MainChannel] Making authentication...", -1)
                    # Authentication.authentication(account, self.server.password, account.socket, logs, self.newAccount)
                    threading.Thread(target=Authentication.authentication, daemon=True,
                                     args=(account, self.server.password, account.socket, logs, self.newAccount)
                                     ).start()
                except socket.timeout:
                    account.socket.close()

        threading.Thread(target=thread, daemon=True).start()

    def RegisterConnectionHandler(self, function: callable):
        self._connectionFunctionTrigger.append(function)

    def RegisterNewAccountHandler(self, function: callable):
        self._connectionFunctionTrigger.append(function)

    def newAccount(self, account: Account):
        self.server.accountManager.add(account)

        for i in self._connectionFunctionTrigger:
            i()
