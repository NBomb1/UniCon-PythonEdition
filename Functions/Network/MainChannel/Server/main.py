import socket as s

from Functions.Network.Accounts.AccountManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.SecurityInfo import SecurityInfo
from Functions.Network.MainChannel.Server.ServerHandlers import ServerInformation
from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.logManager import Logs
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Functions.Network.FileTransfer.FileTransfer import Module

"""
1. Определение программы по уникальному сообщению +
2. Отправка версий встроенных модулей и их сравнение +
3. Проверка пароля +
4. Отправка данных пользователя +
5. Отправка информации о каждом модуле -
6. Подключение по модулям
"""


class ServerMainChannel:
    socket: s.socket = None
    manager: ServerInformation = None

    def __init__(self,
                 logs: Logs,
                 accountManager: AccountManager,
                 ip: str,
                 port: int,
                 maxCon: int,
                 password: str | None,
                 beforeAuth: callable,
                 mcm: ConnectorManager,
                 IPv6: bool,
                 fileTransfer: 'Module'
                 ):
        self.fileTransfer = fileTransfer
        self.mcm = mcm
        self.beforeAuth = beforeAuth
        self.logs = logs
        self.accountManager = accountManager
        self.logs.sendLog(f"[MainChannel] Starting server on {ip}:{port} with {maxCon} max connections.", 0)
        self.logs.sendLog(f"[MainChannel] Starting server on {ip}:{port} with {maxCon} max connections.", -1)

        if password is None:
            password = SecurityInfo.defaultPassword
            self.logs.sendLog("[MainChannel] Using default password.", -1)
        else:
            self.logs.sendLog("[MainChannel] Using custom password.", -1)

        self.logs.sendLog('[MainChannel] Using ' + ('IPv6' if IPv6 else 'IPv4') + ' address.', -1)
        self.socket = s.socket(s.AF_INET if not IPv6 else s.AF_INET6, s.SOCK_STREAM)
        self.logs.sendLog("[MainChannel] Binding address...", -1)
        self.socket.bind((ip, port))
        self.logs.sendLog("[MainChannel] Address bound successfully.", -1)
        self.socket.listen()
        self.accountManager.setMaxConnections(maxCon)
        self.accountManager.updateAccountInfoHandler()
        self.manager = ServerInformation(ip, port, password,
                                         self.socket, accountManager,
                                         self.beforeAuth,
                                         self.mcm, self.fileTransfer)
        self.mcm.setServer()

        self.accountManager.getSelfAccount().setSocket(
            MessageTransfer(
                accountManager,
                self.socket,
                description='Server'
            )
        )

        self.logs.sendLog("[MainChannel] Creating new connection handler...", -1)
        self.manager.handler.handleIncomingConnections(logs)
