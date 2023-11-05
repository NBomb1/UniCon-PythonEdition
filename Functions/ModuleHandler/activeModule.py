from types import ModuleType


class ActiveModule:
    def __init__(self,
                 name: str,
                 ver: str,
                 author: str,
                 obj: object,
                 module: ModuleType,
                 defaultNetworkAuth: bool,
                 isOnlyUI: bool
                 ):
        self.name = name
        self.version = ver
        self.author = author
        self.object = obj
        self.module = module
        self.defaultNetworkAuth = defaultNetworkAuth
        self.isOnlyUI = isOnlyUI
