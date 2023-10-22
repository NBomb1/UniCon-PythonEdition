from Functions.Network.MainChannel.handlers import Handlers
from Functions.Server.AccountManager import AccountManager


class ServerInformation:
    def __init__(self, ip: str, port: int, password: str, handler: Handlers):
        self.ip = ip
        self.port = port
        self.accountManager = AccountManager()
        self.password = password
        self.modules = []
        self.handler = handler
