import socket as s

from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.Info import Info
from Functions.Network.MainChannel.Server.ServerHandlers import ServerInformation
from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.Tools.logManager import Logs

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
                 mcm: ConnectorManager
                 ):
        self.mcm = mcm
        self.beforeAuth = beforeAuth
        self.logs = logs
        self.accountManager = accountManager
        self.logs.sendLog(f"[MainChannel] Starting server on {ip}:{port} with {maxCon} max connections.", 0)
        self.logs.sendLog(f"[MainChannel] Starting server on {ip}:{port} with {maxCon} max connections.", -1)

        if password is None:
            password = Info.defaultPassword
            self.logs.sendLog("[MainChannel] Using default password.", -1)
        else:
            self.logs.sendLog("[MainChannel] Using custom password.", -1)

        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen()
        self.accountManager.setMaxConnections(maxCon)
        self.accountManager.updateAccountInfoHandler()
        self.manager = ServerInformation(ip, port, password, self.socket, accountManager, self.beforeAuth, self.mcm)
        self.mcm.setServer()

        self.accountManager.getSelfAccount().setSocket(MessageTransfer(accountManager, self.socket))

        self.logs.sendLog("[MainChannel] Creating new connection handler...", -1)
        self.manager.handler.handleIncomingConnections(logs)
