from types import ModuleType


class ActiveModule:
    def __init__(self,
                 id_: str,
                 name: str,
                 ver: str,
                 author: str,
                 obj: object,
                 module: ModuleType,
                 defaultNetworkAuth: bool,
                 isUI: bool,
                 isInternal: bool
                 ):
        self.id_ = id_
        self.name = name
        self.version = ver
        self.author = author
        self.object = obj
        self.module = module
        self.defaultNetworkAuth = defaultNetworkAuth
        self.isUI = isUI
        self.isInternal = isInternal
        self.description = module.__doc__
