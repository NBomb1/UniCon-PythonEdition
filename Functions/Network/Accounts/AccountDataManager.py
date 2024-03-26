from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountDataTransfer import AccountDataTransfer
from Functions.Network.Accounts.SelfAccount import SelfAccount


class AccountManager(AccountDataTransfer):
    _NewAccountTrigger = []
    participants: list[Account] = []
    selfAccount: SelfAccount

    def add(self, account: Account):
        self.participants.append(account)
        for func in self._NewAccountTrigger:
            func(account)

    def remove(self, account: Account):
        self.participants.remove(account)

    def findID(self, id_: str):
        for i in self.participants:
            if i.id == id_:
                return i
        return None

    def getSelfAccount(self):
        return self.selfAccount

    def removeAll(self):
        for i in self.participants:
            self.remove(i)

    def addNewAccountFunction(self, func: callable):
        self._NewAccountTrigger.append(func)

    def setSelfAccount(self, selfAccount: SelfAccount):
        self.selfAccount = selfAccount
