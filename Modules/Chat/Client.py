import datetime
from typing import TYPE_CHECKING

from Functions.ModuleHandler.moduleAPI import API
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
        s.registerFunction('chat', self.getMessage)
        s.registerFunction('sys', self.getSysMessage)
        s.handleMessages()
        s.senderHandler()

    def sendMessage(self, message: str, type: str):
        time = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        self.socket.send_message(type,
                                 msg=message,
                                 time=int(time.timestamp())
                                 )

    def getMessage(self, msg):
        self.logMessage(
            msg['nickname'],
            msg['id'],
            msg['msg'],
            datetime.datetime.fromtimestamp(int(msg['time']), datetime.timezone.utc),
            msg['id'] == self.selfAccount.id
        )

    def getSysMessage(self, msg):
        self.module.log(
            msg['msg'],
            # msg['id'],
            # msg['msg'],
            datetime.datetime.fromtimestamp(int(msg['time']), datetime.timezone.utc),
            # msg['id'] == self.selfAccount.id
        )

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
