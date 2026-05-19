import socket
from hashlib import sha256
from traceback import format_exc

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountManager import AccountManager
from Functions.Network.FileTransfer.Data.Actions import Actions
from Functions.Network.FileTransfer.Data.StatesHistory import StatesHistory
from Functions.Network.FileTransfer.Files.Sending.FileSendingContainer import SendingInfo
from Functions.Network.FileTransfer.Files.Sending.SendingFileInfo import SendFileInfo
from Functions.logManager import Logs


class SelfSender(StatesHistory, Actions):
    def __init__(
            self,
            receiver: Account,
            accountManager: AccountManager,
            logs: Logs,
            file_container: SendingInfo,
            code: bytes,
            moduleID: str,
            on_update: callable = None
    ):
        super().__init__(on_update)

        self.logs = logs
        self.receiver = receiver
        self.sender = accountManager.getSelfAccount()
        self.file_container = file_container
        self.code = code
        self.moduleId = moduleID

        self.error_text: None | str = None
        self.transfer_socket: None | socket.socket = None

        self.is_server = accountManager.getIsServer()
        self.account_manager = accountManager
        self.current: SendFileInfo | None = None

    def set_socket(self, s: socket.socket):
        self.transfer_socket = s

    def invite(self):
        """Just sends invite message."""
        assert self.getState() in (self.state_initialised, self.state_serverAccepted), \
            f'Current state is "{self.states_dict_int_to_str.get(self.getState())}" which is unsupportable to invite.'
        s = self.receiver if self.is_server else self.account_manager.getOwner()

        # Creating request on server side
        s.socket.send_message(
            'FileTransfer',
            code=self.code,
            receiver=self.receiver.id,
            action=self.action_create,
            state=self.getState(),
            files=self.file_container.sending_information_format(),
            moduleId=self.moduleId,
        )

    def start_sending(self):
        assert self.transfer_socket is not None, 'File transferring socket is None.'

        try:
            for file in self.file_container:
                self.current = file
                while file.fullSize != file.sentSize:
                    file.updateSentSize(
                        self.transfer_socket.send(
                            file.file.read(
                                1024
                                if file.fullSize - file.sentSize > 1024
                                else file.fullSize - file.sentSize
                            )
                        )
                    )
        except Exception as e:
            self.error_text = format_exc()
            self.updateState(self.state_error, call_function=True)
            self.logs.sendLog(f"[FileTransfer] Something went wrong {self.code} -> {e}.", -3)
            raise e

    def connect(self):
        if self.transfer_socket is not None:
            return

        origin = self.account_manager.getOwner().socket.socket
        s = socket.socket(origin.family, origin.type, origin.proto)
        s.connect(origin.getpeername())
        s.send(sha256(self.code + self.sender.salt).hexdigest().encode())

        self.set_socket(s)
