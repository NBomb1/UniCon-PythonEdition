import socket
from hashlib import sha256
from traceback import format_exc

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountManager import AccountManager
from Functions.Network.FileTransfer.Data.Actions import Actions
from Functions.Network.FileTransfer.Data.StatesHistory import StatesHistory
from Functions.Network.FileTransfer.Files.Receiving import ReceivingFileInfo
from Functions.Network.FileTransfer.Files.Receiving.FileReceivingContainer import ReceivingContainer
from Functions.Network.FileTransfer.Files.Receiving.ReceivingFileInfo import ReceiveFileInfo
from Functions.logManager import Logs


class SelfReceiver(StatesHistory, Actions):
    def __init__(
            self,
            sender: Account,
            accountManager: AccountManager,
            logs: Logs,
            file_container: ReceivingContainer,
            code: bytes,
            moduleID: str,
            on_update: callable = None
    ):
        super().__init__(on_update)

        self.logs = logs
        self.receiver = accountManager.getSelfAccount()
        self.sender = sender
        self.file_container = file_container
        self.code = code
        self.moduleId = moduleID

        self.error_text: None | str = None
        self.transfer_socket: None | socket.socket = None

        self.is_server = accountManager.getIsServer()
        self.current: ReceiveFileInfo | None = None

    def set_socket(self, s: socket.socket):
        self.transfer_socket = s

    def start_receiving(self):
        assert self.transfer_socket is not None, "Transfer socket can't be None"
        assert self.getState() == self.state_sending, "Can't start receiving without sending(5) state."

        # Receive files
        try:
            for file in self.file_container:
                if not self._receive_file(file):
                    return

            if self.is_server:
                self.updateState(self.state_completed, call_function=True)
        except Exception as e:
            print(format_exc())
            self.logs.sendLog(f"[FileTransfer] An error occurred while transferring files. {e}", -3)
            self.logs.sendLog(f"[FileTransfer] Detailed info: {format_exc()}", -3)

    def _receive_file(self, file: ReceivingFileInfo) -> bool:
        """
        Helper method to receive a single file.
        """
        self.current = file
        try:
            while True:

                data = self.transfer_socket.recv(
                    1024
                    if file.fullSize - file.receivedSize > 1024
                    else file.fullSize - file.receivedSize
                )
                file.file.write(data)
                file.updateSentSize(len(data))

                if file.receivedSize == file.fullSize:
                    file.file.close()
                    break

            return True

        except Exception:
            print(format_exc())
            self.updateState(self.state_error, call_function=True)
            return False

    def connect(self):
        origin = self.receiver.socket.socket
        s = socket.socket(origin.family, origin.type, origin.proto)
        s.connect(origin.getpeername())
        s.send(sha256(self.code + self.receiver.salt).hexdigest().encode())

        self.set_socket(s)
