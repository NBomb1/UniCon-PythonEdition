from Functions.Network.Accounts.AccountData import Account


class InviteConnectionInfo:
    def __init__(self, specialCode: str, accountFrom: Account, id_: str, ver: str, accept: callable):
        self.specialCode = specialCode
        self.account = accountFrom
        self.id_ = id_
        self.version = ver
        self.accept = accept
