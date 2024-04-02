from threading import Thread

from Functions.Network.Accounts.AccountAuthentication.Server import ServerAuthentication
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountDataManager import AccountManager


class PingManager:
    account: Account
    accountManager: AccountManager

    def __init__(self, account: Account, accountManager: AccountManager):
        self.account = account
        self.accountManager = accountManager

    def _startChecking(self):
        while True:
            specialCode = ServerAuthentication.Authentication.generate_random_id(8)
