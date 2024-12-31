import socket
import threading

from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.Accounts.AccountAuthentication.Server.PreAuthAccount import PreAccount
from Functions.Network.Accounts.AccountAuthentication.Server.ServerAuthentication import Authentication
from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.logManager import Logs
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Functions.Network.FileTransfer.FileTransfer import Module


class ServerInformation:
    def __init__(self,
                 ip: str,
                 port: int,
                 password: str,
                 s: socket.socket,
                 accountManager: AccountManager,
                 beforeAuth: callable,
                 mc: ConnectorManager,
                 fileTransfer: 'Module'
                 ):
        self.fileTransfer = fileTransfer
        self.ip = ip
        self.port = port
        self.accountManager = accountManager
        self.password = password
        self.modules = []
        self.handler = Handlers(s, self)
        self.beforeAuth = beforeAuth
        self.connectorManager = mc


class Handlers:

    def __init__(self, s: socket.socket, info: ServerInformation):
        self.socket = s
        self.server = info

    def handleIncomingConnections(self, logs: Logs):
        def thread():
            while True:
                try:
                    logs.sendLog("[MainChannel] Waiting for new connections. ", -1)
                    account = PreAccount(self.socket.accept())  # Creating Pre Account for others Modules
                    self.server.beforeAuth(account)
                    logs.sendLog(f"[MainChannel] "
                                 f"Got new {'module ' if account.stopAuth else ''}connection from "
                                 f"{account.ip}:{account.port}", -1)
                    if account.stopAuth:
                        continue

                    threading.Thread(
                        target=Authentication.authentication,
                        args=(
                            account,
                            self.server.password,
                            account.socket,
                            logs,
                            self.server.accountManager,
                            self.server.connectorManager,
                            self.server.fileTransfer
                        ),
                        daemon=True).start()

                except socket.timeout:
                    account.socket.close()
                except OSError:
                    return

        threading.Thread(target=thread, daemon=True).start()
