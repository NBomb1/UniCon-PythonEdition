import socket
import threading

from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.Accounts.AccountAuthentication.Server.PreAuthAccount import PreAccount
from Functions.Network.Accounts.AccountAuthentication.Server.ServerAuthentication import Authentication
from Functions.Network.Accounts.AccountData import Account
from Functions.Tools.logManager import Logs


class ServerInformation:
    def __init__(self, ip: str, port: int, password: str, s: socket.socket, accountManager: AccountManager):
        self.ip = ip
        self.port = port
        self.accountManager = accountManager
        self.password = password
        self.modules = []
        self.handler = Handlers(s, self)


class Handlers:
    isWorking = False

    def __init__(self, s: socket.socket, info: ServerInformation):
        self.socket = s
        self.server = info
        self._connectionFunctionTrigger = []

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
                    logs.sendLog(f"[MainChannel] Got new connection from {account.ip}:{account.port}", -1)
                    for i in self._connectionFunctionTrigger:
                        i()  # getting all functions to call
                    logs.sendLog("[MainChannel] Starting authentication...", -1)

                    threading.Thread(
                        target=Authentication.authentication,
                        args=(
                            account,
                            self.server.password,
                            account.socket,
                            logs,
                            self.server.accountManager
                        ),
                        daemon=True).start()

                except socket.timeout:
                    account.socket.close()

        threading.Thread(target=thread, daemon=True).start()

    def RegisterConnectionHandler(self, function: callable):
        self._connectionFunctionTrigger.append(function)

    def newConnection(self, account: Account):
        self.server.accountManager.add(account)

        for i in self._connectionFunctionTrigger:
            i()
