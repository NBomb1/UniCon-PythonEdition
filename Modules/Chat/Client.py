import datetime
from typing import TYPE_CHECKING

from Functions.ModuleHandler.moduleAPI import API
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Network.DataTransfer import MessageTransfer

if TYPE_CHECKING:
    from Modules.Chat.main import Module


class Client:
    def __init__(self, api: API, module: 'Module', s: MessageTransfer):
        self.ModuleId = module.id_
        self.module: 'Module' = module
        self.api = api
        self.logs = api.getLogs()
        self.selfAccount: SelfAccount = api.getAccountManager().getSelfAccount()
        self.socket = s

        self.participants: list[Account] = []
        self.accountManager = self.api.getAccountManager()

        s.registerFunction('chat', self.get_chat_message)
        # s.registerFunction('close', self.get_participant_message)
        s.registerFunction('add', self.get_participant_message)
        s.registerFunction('add-m', self.get_participant_message)
        s.registerFunction('rem', self.get_participant_message)
        s.handleMessages()
        s.senderHandler()

    def sendMessage(self, message: str, type: str):
        time = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        self.socket.send_message(type,
                                 msg=message,
                                 time=int(time.timestamp())
                                 )

    def get_chat_message(self, msg):
        self.logMessage(
            msg['nickname'],
            msg['id'],
            msg['msg'],
            datetime.datetime.fromtimestamp(int(msg['time']), datetime.timezone.utc),
            msg['id'] == self.selfAccount.id
        )

    def get_participant_message(self, m: dict):
        type_ = m['type']
        info = m['msg']
        time = m.get('time')
        account = self.accountManager.findByID(info)

        if account is None and type_ in ('add', 'rem'):
            self.logs.sendLog('[Chat] Unable to find participant in accountManager list.', 0)
            return

        if type_ == 'add':
            self.participants.append(account)
            self.module.update_participants(self.participants, self.selfAccount)
            self.module.log(f'{account.nickname} - {account.id} connected to the chat.',
                            datetime.datetime.fromtimestamp(time, datetime.timezone.utc))
        elif type_ == 'add-m':
            self.participants.extend(tuple(map(lambda x: self.accountManager.findByID(x), info)))
            self.module.update_participants(self.participants, self.selfAccount)
        elif type_ == 'rem':
            try:
                self.participants.remove(account)
            except ValueError:
                pass
            self.module.log(f'{account.nickname} - {account.id} disconnected from the chat.',
                            datetime.datetime.fromtimestamp(time, datetime.timezone.utc))
            self.module.update_participants(self.participants, self.selfAccount)

    def logMessage(self, nickname: str, id: str, message: str, time: datetime.datetime, markGreen=False):
        time = time.astimezone(tz=None)
        nicknameList = list(map(lambda x: x.nickname, self.api.getAccountManager().getParticipants()))
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
