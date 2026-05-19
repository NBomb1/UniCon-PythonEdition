from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Network.DataTransfer import MessageTransfer


class AccountDataHandler:
    # specially for server side
    participants: list[Account] = []
    selfAccount: SelfAccount

    #  Functions/Network/Accounts/AccountManager.py
    add: callable
    findByID: callable
    _disconnectAccount: callable

    def accountHandler(self, msg: dict[str, str]):
        if msg.get('_all') is None:
            account: Account = self.findByID(msg['id'])
            if account is None:  # if account is not present we create one
                account = Account(
                    MessageTransfer(self, None),
                    None,
                    None,
                    None,
                    None,
                    msg['id'],
                    None
                )
                self.add(account)

            if msg['what'] == Account.what_ping:
                account.update_ping(msg['data'])
            if msg['what'] == Account.what_nickname:
                account.updateNickname(msg['data'])
            if msg['what'] == 'disconnect':  # account has been disconnected
                account: Account = self.findByID(msg['id'])
                self._disconnectAccount(self.findByID(msg['id']))
        else:
            for i in msg['_all']:
                account: Account = self.findByID(i['id'])
                if account is None:
                    account = Account(MessageTransfer(self, None)
                    , None, None, None, None, i['id'], None)
                    self.add(account)
                for info in i:
                    if info == Account.what_nickname:
                        account.updateNickname(i[info])
                    if info == Account.what_ping:
                        account.update_ping(i[info])
                    if info == Account.what_pc_name:
                        account.updatePcName(i[info])
                    if info == Account.what_tag:
                        account.updateTags(i[info])
