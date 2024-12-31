from Functions.Network.Accounts.AccountAuthentication.Client.AuthenticationPassing import Authentication
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.SecurityInfo import SecurityInfo
from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.logManager import Logs
import socket as s
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UI.MainMenu import MainMenu


class ClientMainChannel:
    socket: s = None

    def __init__(
            self,
            logs: Logs,
            account: AccountManager,
            ip: str,
            port: int,
            mc: ConnectorManager,
            mainMenu: 'MainMenu',
            password: str | None,
            IPv6: bool,
    ):
        self.logs = logs
        self.mainMenu = mainMenu
        self.accountManager = account
        self.mc = mc
        self.logs.sendLog(f"[MainChannel] Connecting to server {ip}:{port}", -1)

        if password is None:
            password = SecurityInfo.defaultPassword
            self.logs.sendLog("[MainChannel Client] Using default password.", -1)
        else:
            self.logs.sendLog("[MainChannel Client] Using custom password.", -1)

        self.logs.sendLog('[MainChannel] Using ' + ('IPv6' if IPv6 else 'IPv4') + ' address.', -1)
        self.socket = s.socket(s.AF_INET if not IPv6 else s.AF_INET6, s.SOCK_STREAM)
        self.logs.sendLog("[MainChannel Client] Connecting to the server...", -1)
        self.socket.connect((ip, port))
        self.logs.sendLog("[MainChannel Client] Connected to the server.", -1)
        self.messageTransfer = MessageTransfer(account, self.socket, description='Client main channel')

        self.messageTransfer.registerType('ModuleConnector')
        self.messageTransfer.registerType('FileTransfer')
        self.messageTransfer.registerType('close')
        self.messageTransfer.registerType('account')

        self.messageTransfer.senderHandler()
        self.accountManager.getSelfAccount().setSocket(self.messageTransfer)

        self.accountManager.setMaxConnections(5000)
        Authentication(self.messageTransfer, self.logs, password, self.mainMenu, account).start()

        self.messageTransfer.registerFunction('close', self.accountManager._disconnectedFromServer)  # it's fine
        self.messageTransfer.registerFunction('account', self.accountManager.accountHandler)
        # self.messageTransfer.registerFunction('FileTransfer', self.mainMenu.fileTransfer.mainChannelResponses)

        mc.setClient(self.messageTransfer)
