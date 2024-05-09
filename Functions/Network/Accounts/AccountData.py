from Functions.ModuleHandler.activeModule import ActiveModule
from Functions.Network.DataTransfer import MessageTransfer


class Account:
    socket: MessageTransfer
    ip: str
    port: int
    nickname: str
    pc_name: str
    id: str
    ping: int
    on_ping_update_functions = []

    def __init__(
            self,
            socket: MessageTransfer,
            ip: str,
            port: int,
            nickname: str,
            pc_name: str,
            id_: str,
            salt: bytes | None,
            tags: list = None
    ):
        self.socket = socket  # for server only
        self.ip = ip
        self.port = port
        self.nickname = nickname
        self.pc_name = pc_name
        self.id = id_
        self.salt = salt  # for server only
        self.ping = -1  # updates
        self.tags = tags if tags is not None else []  # can be used for special perms
        self.extraConnections: dict[str, list[socket.socket]] = {}

    def update_ping(self, ping: int):
        if self.ping != ping:
            self.ping = ping
            for func in self.on_ping_update_functions:
                func(self)

    def add_on_ping_update_function(self, func):
        self.on_ping_update_functions.append(func)

    def remove_on_ping_update_function(self, func):
        self.on_ping_update_functions.remove(func)

    def updateNickname(self, nickname: str):
        self.nickname = nickname

    def addExtraConnection(self, moduleId: str, s: MessageTransfer):
        self.extraConnections.setdefault(moduleId, []).append(s)
