from Functions.Network.Server.AccountAuthentication.Account import Account


class AccountManager:
    participants: list[Account] = []

    def add(self, account: Account):
        self.participants.append(account)

    def remove(self, account: Account):
        self.participants.remove(account)

    def findID(self, id_: str):
        for i in self.participants:
            if i.id == id_:
                return i
        return None
