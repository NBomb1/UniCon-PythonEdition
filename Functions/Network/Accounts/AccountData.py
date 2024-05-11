from threading import Thread

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
    accountUpdated: list[callable] = []

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
        self.extraConnections: dict[str, list[MessageTransfer]] = {}

    def update_ping(self, ping: int):
        if self.ping != ping:
            self.ping = ping
            self.accountHasBeenUpdated()

    def addTag(self, tag: str):
        if tag in self.tags:
            raise Exception(f"tag {tag} is already in list!\nlist: {self.tags}\ntag: '{tag}'")
        self.tags.append(tag)

    def updateNickname(self, nickname: str):
        self.nickname = nickname
        self.accountHasBeenUpdated()

    def addExtraConnection(self, moduleId: str, s: MessageTransfer):
        self.extraConnections.setdefault(moduleId, []).append(s)
        self.accountHasBeenUpdated()

    def removeExtraConnection(self, moduleId: str, s: MessageTransfer):
        self.extraConnections.get(moduleId).remove(s)
        self.accountHasBeenUpdated()

    def addUpdatedAccount(self, func: callable):
        self.accountUpdated.append(func)

    def removeUpdatedAccount(self, func: callable):
        self.accountUpdated.append(func)

    def accountHasBeenUpdated(self):
        for func in self.accountUpdated:
            Thread(target=func, args=(self, ), daemon=True).start()
