import socket

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.FileTransfer.Data.Actions import Actions
from Functions.Network.FileTransfer.Data.StatesHistory import StatesHistory
from Functions.Network.FileTransfer.Files.ClientToClient.ClientToClientContainer import ClientToClientContainer
from Functions.logManager import Logs


class ClientToClient(StatesHistory, Actions):
    def __init__(
            self,
            sender: Account,
            receiver: Account,
            accountManager: AccountManager,
            logs: Logs,
            file_container: ClientToClientContainer,
            code: bytes,
            moduleID: str,
            on_update: callable = None
    ):
        super().__init__(on_update)

        self.logs = logs
        self.receiver = receiver
        self.sender = sender
        self.file_container = file_container
        self.code = code
        self.moduleId = moduleID

        self.error_text: None | str = None

        self.transfer_socket_receiver: socket.socket | None = None
        self.transfer_socket_sender: socket.socket | None = None

        self.is_server = accountManager.getIsServer()
        self.current = 0

    def add_connection(self, s: socket.socket, is_sender: bool):
        if is_sender:
            self.transfer_socket_sender = s
            self.receiver.socket.send_message(
                'FileTransfer',
                code=self.code,
                sender=self.sender.id,
                receiver=self.receiver.id,
                action=self.action_create,
                state=self.getState(),
                files=self.file_container.sending_information_format(),
                moduleId=self.moduleId,
            )
            print('sender connected')
        else:
            self.transfer_socket_receiver = s
            print('receiver connected')

        if self.transfer_socket_receiver is not None and self.transfer_socket_sender is not None:
            print('starting transfer')
            self.start_transfer()

    def start_transfer(self):
        self.send_sending_state(self.receiver.socket)
        self.send_sending_state(self.sender.socket)

        all_bytes = self.file_container.calculate_bytes()
        received_bytes = 0

        while all_bytes >= received_bytes:
            self.transfer_socket_receiver.send(
                self.transfer_socket_sender.recv(
                    1024 if all_bytes - received_bytes > 1024 else all_bytes - received_bytes
                )
            )
            self.current = all_bytes / received_bytes
        self.send_finish(self.receiver.socket)
        self.send_finish(self.sender.socket)
        self.updateState(self.state_completed, call_function=True)

    def send_sending_state(self, s: MessageTransfer):
        s.send_message(
            'FileTransfer',
            code=self.code,
            action=self.action_update,
            state=self.state_sending,
        )

    def send_finish(self, s):
        s.send_message(
            'FileTransfer',
            code=self.code,
            action=self.action_finish,
            state=self.state_completed,
        )
