import socket as s
from Functions.Network.Info import Info
from Functions.Network.Server.MainChannel.ServerHandlers import ServerInformation
from Functions.Tools.logManager import Logs

"""
1. Определение программы по уникальному сообщению +
2. Отправка версий встроенных модулей и их сравнение +
3. Проверка пароля +
4. Отправка информации о каждом модуле -
5. Подключение по модулям
"""


class MainChannel:
    socket: s.socket = None
    manager: ServerInformation = None

    def __init__(self, logs: Logs, ip: str, port: int, listeners: int, password: str | None):
        self.logs = logs

        if password is None:
            password = Info.defaultPassword
            self.logs.sendLog("[MainChannel] Using default password.", -1)
        else:
            self.logs.sendLog("[MainChannel] Using custom password.", -1)

        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.logs.sendLog(f"[MainChannel] Starting server on {ip}:{port} with {listeners} listeners.", 0)
        self.socket.bind((ip, port))
        self.socket.listen(listeners)
        self.manager = ServerInformation(ip, port, password, self.socket)

        self.logs.sendLog("[MainChannel] Creating new connection handler...", -1)
        self.manager.handler.handleIncomingConnections(logs)
