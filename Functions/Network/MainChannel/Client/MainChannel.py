from Functions.Network.Accounts.AccountAuthentication.Client.AuthenticationPassing import Authentication
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.Info import Info
from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.Tools.logManager import Logs
import socket as s


class ClientMainChannel:
    socket: s = None

    def __init__(
            self,
            logs: Logs,
            account: AccountManager,
            ip: str,
            port: int,
            mc: ConnectorManager,
            askPassword: callable,
            password: str | None,
    ):
        self.logs = logs
        self.askPassword = askPassword
        self.accountManager = account
        self.mc = mc
        logs.sendLog(f"Connecting to server {ip}:{port}", -1)

        if password is None:
            password = Info.defaultPassword
            self.logs.sendLog("[MainChannel Client] Using default password.", -1)
        else:
            self.logs.sendLog("[MainChannel Client] Using custom password.", -1)

        self.socket = s.socket()
        self.logs.sendLog("[MainChannel Client] Connecting to the server...", -1)
        self.socket.connect((ip, port))
        self.messageTransfer = MessageTransfer(account, self.socket)

        self.messageTransfer.registerType('ModuleConnector')
        self.messageTransfer.registerType('close')

        self.messageTransfer.senderHandler()

        self.accountManager.setMaxConnections(50)
        Authentication(self.messageTransfer, self.logs, password, self.askPassword, account).start()
        self.messageTransfer.registerFunction('close', self.accountManager._disconnectedFromServer)  # it's ok
        mc.setClient(self.messageTransfer)
