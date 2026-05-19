from threading import Thread
from time import sleep

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.SelfAccount import SelfAccount


class AccountDataTransfer:
    # specially for server side
    participants: list[Account] = []
    selfAccount: SelfAccount
    rights = {
        '_all': [
            Account.what_pc_name,
            Account.what_nickname,
            # Account.what_ping,
            Account.what_tag,
        ]
    }

    def getAllInfoAccount(self, tags_: list[str]) -> list[dict[str: str]]:
        informationToGet = []
        send = []
        tags = ['_all']
        tags.extend(tags_)
        for tag in tags:
            if tag in self.rights:
                informationToGet.extend(self.rights.get(tag))
        informationToGet = set(informationToGet)

        tempAccountList = [self.selfAccount]
        tempAccountList.extend(self.participants)

        for i in tempAccountList:
            put = {}
            for info in informationToGet:
                put[info] = getattr(i, info)
            put['id'] = i.id
            send.append(put)
        return send

    def updateAccountInfoHandler(self):
        self.accountDisconnectedTrigger(self._accountDisconnection)

        def handler1():
            self_account = self.getSelfAccount()
            while self.getSelfAccount() is self_account:
                self._sendAllInfo()
                sleep(60)

        Thread(target=handler1, daemon=True).start()

    def _sendPingInfo(self, account: Account):
        for i in self.participants:
            i.socket.send_message('account', id=account.id, ping=account.ping)

    def _sendUpdatedInfo(self, account: Account, what: str):
        # if what == 'ping':
        #     return
        if what == Account.what_conn:
            return
        for i in self.participants:
            i.socket.send_message('account', id=account.id, what=what, data=getattr(account, what))

    def _sendAllInfo(self):
        for i in self.participants:
            i.socket.send_message('account', _all=self.getAllInfoAccount(i.tags))

    def _accountDisconnection(self, account: Account):
        for i in self.participants:
            if i == account:
                continue
            i.socket.send_message('account', id=account.id, what='disconnect')
