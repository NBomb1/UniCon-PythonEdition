import datetime
from traceback import format_exc

from Functions.ModuleHandler.moduleAPI import API
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Network.DataTransfer import MessageTransfer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Modules.Chat.main import Module


class Server:
    participants: list[MessageTransfer] = []

    def __init__(self, api: API, module: 'Module'):
        self.ModuleId = module.id_
        self.module: 'Module' = module
        self.api = api
        self.logs = api.getLogs()
        self.selfAccount: SelfAccount = api.getAccountManager().getSelfAccount()

    def errorOccurred(self, exception: Exception, m: MessageTransfer):
        self.logs.sendLog(f'[Chat] An error occurred in {m.account.id}: {exception}', -1)
        self.clientDisconnected(m)

    def clientDisconnected(self, m):
        account = m.account
        self.logs.sendLog(f'Client {account.nickname} - {account.id} disconnected from the chat.', -1)
        try:
            self.participants.remove(m)
        except ValueError:
            pass
        self.sendMessage(f'Client {account.nickname} - {account.id} disconnected from the chat.', 'sys')

    def add(self, participant: MessageTransfer):
        self.participants.append(participant)
        participant.handleMessages()
        participant.senderHandler()
        participant.registerErrorFunction(self.errorOccurred)
        participant.registerFunction('chat', self.getMessage)
        participant.registerFunction('close', self.clientDisconnected)
        self.sendMessage(
            f'Client {participant.account.nickname} - {participant.account.id} connected to the chat.',
            'sys'
        )

    def sendMessage(self, message: str, type: str):
        time = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        for i in self.participants:
            try:
                i.send_message(type,
                               msg=message,
                               nickname=self.selfAccount.nickname,
                               id=self.selfAccount.id,
                               time=int(time.timestamp())
                               )
            except Exception as e:
                self.logs.sendLog(f'[Chat] An exception occurred while sending message to {i.account.id}', -1)
                self.logs.sendLog(f'[Chat] {i.account.id_} exception: {format_exc()}', -1)
                self.errorOccurred(e, i)
        if type != 'sys':
            self.logMessage(self.selfAccount.nickname, self.selfAccount.id, message, time, True)
        else:
            self.module.log(message, time)

    def getMessage(self, m):
        try:
            time = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
            account: Account = m['_account']
            nickname = account.nickname
            id_ = account.id
            message = m['msg']
            for participant in self.participants:
                participant.send_message(
                        'chat',
                        msg=message,
                        id=id_,
                        nickname=nickname,
                        time=int(time.timestamp())
                )
            self.logMessage(account.nickname, account.id, message, time)
        except Exception as e:
            self.logs.sendLog(f'[Chat] An exception occurred while sending message from {m["_account"].id_}', -1)
            self.logs.sendLog(f'[Chat] {m["_account"].id_} exception: {format_exc()}', -1)
            self.errorOccurred(e, m)

    def stop(self):
        self.logs.sendLog('[Chat] Closing connection chat.', -1)
        for i in self.participants:
            i.send_message(
                'close',
                msg='Chat closed by server.'
            )
            i.account.removeExtraConnectionExact(self.ModuleId, i)
        self.participants.clear()
        self.logs.sendLog('[Chat] Chat closed successfully.', -1)

    def logMessage(self, nickname: str, id: str, message: str, time: datetime.datetime, markGreen=False):
        try:
            time = time.astimezone(tz=None)
            nicknameList = list(map(lambda x: x.account.nickname, self.participants))
            nicknameList.append(self.api.getAccountManager().getSelfAccount().nickname)  # all nicknames
            if nicknameList.count(nickname) > 1:
                self.module.messageID(message, id, time, markGreen)
            else:
                self.module.message_(
                    message,
                    nickname,
                    time,
                    markGreen
                )
        except AttributeError:
            self.stop()

    # def sendMessage(self, type: str, id_: str, msg: str, nickname: str, time: datetime):
