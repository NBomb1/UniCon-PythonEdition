from Functions.Network.Accounts.AccountDataManager import AccountManager


class TriggerManager:
    def __init__(self, accountManager: AccountManager):
        self.accountManager = accountManager

    def accountAddedTrigger(self, func: callable):
        self.accountManager.addNewAccountFunction(func)
