import hashlib
import socket
from functools import partial
from traceback import format_exc
from typing import TYPE_CHECKING

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.FileTransfer.Data.Actions import Actions
from Functions.Network.FileTransfer.Files.ClientToClient.ClientToClientContainer import ClientToClientContainer
from Functions.Network.FileTransfer.Files.Receiving.FileReceivingContainer import ReceivingContainer
from Functions.Network.FileTransfer.Requests.ClientToClient import ClientToClient
from Functions.Network.FileTransfer.Requests.RequestsRegistering import RequestRegistering
from Functions.Network.FileTransfer.Requests.SelfReceiver import SelfReceiver
from Functions.Network.FileTransfer.Requests.SelfSender import SelfSender
from Functions.logManager import Logs

if TYPE_CHECKING:
    from Functions.Network.FileTransfer.FileTransfer import FileTransfer


class ServerHandler(Actions, RequestRegistering):

    def __init__(self, logs: Logs, fileTransfer: 'FileTransfer'):
        self.accountManager = fileTransfer.accountManager
        self.moduleLoader = fileTransfer.api.getModuleLoader()
        self.logs = logs
        self.fileTransfer = fileTransfer

    def on_request_update(self, code: bytes, state: int):
        print(f"on_request_update: {state}")
        request = self.all_requests.get(code)
        assert request is not None, "Request can't be None."
        s = request.sender if isinstance(request, SelfReceiver) else request.receiver

        if state == self.state_error:
            request.receiver.socket.send_message(
                'FileTransfer',
                code=code,
                action=self.action_finish,
                state=self.state_error,
                reason=request.error_text
            )
            request.is_finished = True
        elif state == self.state_serverAccepted:
            if isinstance(request, (SelfReceiver, ClientToClient)):
                request.sender.socket.send_message(
                    'FileTransfer',
                    code=code,
                    action=self.action_update,
                    state=self.state_serverAccepted
                )
        elif state in (self.state_cancelled, self.state_completed, self.state_timed_out_client_response,
                       self.state_clientDeclined):
            s.socket.send_message(
                'FileTransfer',
                code=code,
                action=self.action_finish,
                state=state,
                reason=request.error_text
            )

            # calling functions if request is finished
            for function in self.fileTransfer.trigger_requestRemoved:
                function(request)
            if self.all_requests.get(request.code):
                self.all_requests.pop(request.code)
        elif state == self.state_sending:
            s.socket.send_message(
                'FileTransfer',
                code=code,
                action=self.action_update,
                state=self.state_sending
            )
            if isinstance(request, SelfSender):
                request.start_sending()
        else:
            raise ValueError(f"Out of if clause: \ncode: {code}\nstate: {self.states_dict_int_to_str.get(state)} "
                             f"{state}.")

    def check_special_code(self, msg: str, s: socket.socket):
        assert isinstance(msg, str), f'Wrong instance {type(msg).__name__} != str.'

        # Checking requests that are waiting for connection.
        for request in filter(lambda x: x.getState() == self.state_serverAccepted, self.all_requests.values()):
            sender_code = hashlib.sha256(
                request.code + request.sender.salt).hexdigest() if request.sender.salt is not None else None
            receiver_code = hashlib.sha256(
                request.code + request.receiver.salt).hexdigest() if request.receiver.salt is not None else None

            if msg in (sender_code, receiver_code):
                print(f'{"sender" if msg == receiver_code else "receiver"}: {msg}')
                # TODO: DELETE AND REWORK
                request.transfer_socket = s
                print(f"name: {type(request).__name__}")
                if isinstance(request, SelfSender):
                    request.updateState(self.state_sending, call_function=True)
                    request.start_sending()
                elif isinstance(request, SelfReceiver):
                    request.updateState(self.state_sending, call_function=True)
                    request.start_receiving()
                elif isinstance(request, ClientToClient):
                    request.add_connection(s, msg == sender_code)
                return True  # Code request has been found.
            print(  # TODO: DELETE PRINT
                f'ELSE\n'
                f'msg: {msg}\n'
                f'sender-code: {sender_code}\n'
                f'receiver-code: {receiver_code}'
            )
            continue  # Isn't a right request.

        return False  # No code request was found.

    def checking_file_transfer_type(self, msg: dict):
        sender: Account = msg.get('_account')
        code = msg.get('code')
        files = msg.get('files')
        action = msg.get('action')
        state = msg.get('state')
        moduleID = msg.get('moduleId')
        receiver = msg.get('receiver')
        reason = msg.get('reason')

        try:
            if action == self.action_create:

                if not self.fileTransfer.is_enabled.savedData:
                    self.sendDecline(code, sender.socket, "FileTransfer is turned off.")
                    return

                receiver = self.accountManager.findByID(receiver)

                # Checking receiver
                if receiver is None:
                    self.sendDecline(code, sender.socket, "Receiver wasn't found.")
                    return

                # Module checking 1
                module = self.moduleLoader.findById(moduleID)
                if module is None and not self.fileTransfer.allowUnknownModules and isinstance(receiver, SelfAccount):
                    self.sendDecline(code, sender.socket, "Can't accept request with unknown module.")
                    return

                # Module checking 2
                if (
                        module is None
                        and not
                        self.fileTransfer.allowUnknownModules_serverSide
                        and
                        isinstance(receiver, Account)
                ):
                    self.sendDecline(code, sender.socket, "Unknown modules are not allowed.")
                    return

                # Checking code
                if self.all_requests.get(code) is not None:
                    self.sendDecline(
                        code, sender.socket, "Request with this code is already existing. Try creating a new one."
                    )
                    return

                # Checking receiver and creating request
                if isinstance(receiver, SelfAccount):
                    request = SelfReceiver(
                        sender,
                        self.accountManager,
                        self.logs,
                        ReceivingContainer(files, receiver, sender),
                        code,
                        moduleID,
                        partial(self.on_request_update, code)
                    )

                    self.all_requests[code] = request
                elif isinstance(receiver, Account):
                    request = ClientToClient(
                        sender,
                        receiver,
                        self.accountManager,
                        self.logs,
                        ClientToClientContainer(files),
                        code,
                        moduleID,
                        partial(self.on_request_update, code)
                    )

                    self.all_requests[code] = request

                    self.all_requests.pop(request.code)
                else:
                    return
                request.updateState(self.state_serverAccepted, call_function=True)

                self.checking_requests()

                # calling function when request is created
                for function in self.fileTransfer.trigger_requestAdded:
                    function(request)
                return

            request = self.all_requests.get(code)

            if action in (self.action_update, self.action_finish):
                # Checking for request existence
                if request is None and action == self.action_update:
                    self.sendError(code, sender.socket, "Request is not found.")
                    return
                if sender not in (request.receiver, request.sender):
                    self.sendError(code, sender.socket, "You are not a participant of this request.")
                    return
            else:
                self.sendError(code, sender.socket, "Action not in list.")
                return

            if action == self.action_update:
                # TODO: Checking states
                if reason:
                    request.error_text = reason
                    request.is_finished = True
                request.updateState(state, call_function=True)
            elif action == self.action_finish:
                if reason:
                    request.error_text = reason
                request.is_finished = True
                request.updateState(state)

                for function in self.fileTransfer.trigger_requestRemoved:
                    function(request)
                if self.all_requests.get(request.code):
                    self.all_requests.pop(request.code)
        except Exception as e:
            self.sendError(code, sender.socket, e.__str__())
            print(format_exc())
            raise e

    def sendError(self, code: str, receiver: MessageTransfer, reason: str):
        receiver.send_message(
            'FileTransfer',
            code=code,
            action=self.action_finish,
            state=self.state_error,
            reason=reason
        )

    def sendDecline(self, code: str, receiver: MessageTransfer, reason: str):
        receiver.send_message(
            'FileTransfer',
            code=code,
            action=self.action_finish,
            state=self.state_serverDeclined,
            reason=reason
        )
