import socket as s
from Functions.Network.MainChannel.handlers import Handlers
from Functions.Server.ServerPrefences import ServerInformation
from Functions.Network.MainChannel.Info import Info

"""
1. Определение программы по уникальному сообщению +
2. Отправка версий встроенных модулей и их сравнение +
3. Проверка пароля /
4. Отправка информации о каждом модуле
5. Подключение по модулям
"""


class MainChannel:
    socket: s.socket = None
    _handler: Handlers = None
    manager: ServerInformation = None

    def __init__(self, ip: str, port: int, listeners: int, password: str | None):
        password = Info.defaultPassword if password is None else password
        socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        socket.bind((ip, port))
        socket.listen(listeners)
        self.manager = ServerInformation(ip, port, password, Handlers(socket, self.manager))

        self.manager.handler.handleIncomingConnections()
