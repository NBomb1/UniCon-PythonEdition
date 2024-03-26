from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.SelfAccount import SelfAccount


class AccountDataTransfer:
    participants: list[Account] = []
    selfAccount: SelfAccount

    def getAllInfoAccount(self) -> list[dict[str: str]]:
        info = []
        for account in self.participants:
            info.append(
                {
                    'id': account.id,
                    'pc_name': account.pc_name,
                    'nickname': account.nickname
                }
            )
        return info
