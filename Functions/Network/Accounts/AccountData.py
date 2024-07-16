from threading import Thread

from Functions.Network.DataTransfer import MessageTransfer


class Account:
    # all possible given arguments by default
    what_pc_name = 'pc_name'
    what_id = 'id'
    what_ip = 'ip'
    what_port = 'port'

    what_nickname = 'nickname'
    what_ping = 'ping'
    what_tag = 'tags'
    what_conn = 'extraConnections'

    socket: MessageTransfer
    ip: str
    port: int
    nickname: str
    pc_name: str
    id: str
    ping: int

    def __init__(
            self,
            socket: MessageTransfer | None,
            ip: str | None,
            port: int | None,
            nickname: str | None,
            pc_name: str | None,
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
        self.on_ping_update_functions = []
        self.accountUpdated: list[callable] = []
        self.socket.registerAccount(self)

    def update_ping(self, ping: int):
        if self.ping == ping:
            return
        self.ping = ping
        self.accountHasBeenUpdated(self.what_ping)

    def addTag(self, tag: str):
        if not tag:
            raise ValueError(f"tag can't be empty!")
        if tag in self.tags:
            raise ValueError(f"tag {tag} is already in list!\nlist: {self.tags}\ntag: '{tag}'")
        if tag[0] == '_':
            raise ValueError(f"tag {tag} can't start with '_'!")

        self.tags.append(tag)
        self.accountHasBeenUpdated(self.what_tag)

    def removeTag(self, tag: str):
        if tag not in self.tags:
            raise ValueError(f"tag {tag} is not in list!\nlist: {self.tags}\ntag: '{tag}'")
        self.tags.remove(tag)
        self.accountHasBeenUpdated(self.what_tag)

    def updateTags(self, tags: list):
        self.tags.clear()
        for tag in tags:
            self.addTag(tag)

    def updateNickname(self, nickname: str):
        if nickname == self.nickname:
            return
        self.nickname = nickname
        self.accountHasBeenUpdated(self.what_nickname)

    def updatePcName(self, pc_name: str):
        if pc_name == self.pc_name:
            return
        self.pc_name = pc_name
        self.accountHasBeenUpdated(self.what_pc_name)

    def addExtraConnection(self, moduleId: str, s: MessageTransfer):
        self.extraConnections.setdefault(moduleId, []).append(s)
        self.accountHasBeenUpdated(self.what_conn)

    def removeExtraConnectionExact(self, moduleId: str, s: MessageTransfer):
        self.extraConnections.get(moduleId).remove(s)
        try:
            s.socket.close()
        except OSError:
            pass
        self.accountHasBeenUpdated(self.what_conn)

    def addUpdatedAccount(self, func: callable):
        self.accountUpdated.append(func)

    def removeUpdatedAccount(self, func: callable):
        self.accountUpdated.remove(func)

    def accountHasBeenUpdated(self, what: str):
        if what == self.what_conn:
            print(f'updating conns\n{self.extraConnections}')
            keys = self.extraConnections.copy().keys()
            for i in keys:
                if not self.extraConnections.get(i):
                    self.extraConnections.pop(i)

        for func in self.accountUpdated:
            Thread(target=func, args=(self, what), daemon=True).start()

    def removeExtraConnection(self, s: MessageTransfer):
        for key in self.extraConnections.keys():
            for conn in self.extraConnections[key]:
                if s == conn:
                    self.extraConnections.get(key).remove(conn)
                    try:
                        conn.socket.close()
                    except OSError:
                        pass
                    self.accountHasBeenUpdated(self.what_conn)
                    return
