from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.SelfAccount import SelfAccount


class AccountDataTransfer:
    participants: list[Account] = []
    selfAccount: SelfAccount

    def getAllInfoAccount(self) -> list[dict[str: str]]:
        info = []
        temp = [self.selfAccount]
        temp.extend(self.participants)
        for account in temp:
            info.append(
                {
                    'id': account.id,
                    'pc_name': account.pc_name,
                    'nickname': account.nickname,
                    'tags': account.tags
                }
            )
        return info
