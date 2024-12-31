from functools import partial
from time import sleep
from traceback import format_exc
from typing import TYPE_CHECKING

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.FileTransfer.Data.Actions import Actions
from Functions.Network.FileTransfer.Files.Receiving.FileReceivingContainer import ReceivingContainer
from Functions.Network.FileTransfer.Requests.RequestsRegistering import RequestRegistering
from Functions.Network.FileTransfer.Requests.SelfReceiver import SelfReceiver
from Functions.Network.FileTransfer.Requests.SelfSender import SelfSender
from Functions.logManager import Logs

if TYPE_CHECKING:
    from Functions.Network.FileTransfer.FileTransfer import FileTransfer


class ClientHandler(Actions, RequestRegistering):
    # all_requests: dict[bytes, SelfSender | SelfReceiver] = {}  # TODO: New classes must be added
    # sendingRequests: dict[bytes, SelfSender] = {}
    # receivingRequests: dict[bytes, SelfReceiver] = {}
    # otherRequests: dict = {}

    def __init__(self, accountManager: AccountManager, logs: Logs, fileTransfer: 'FileTransfer'):
        self.accountManager = accountManager
        self.logs = logs
        self.fileTransfer = fileTransfer
        self.moduleLoader = fileTransfer.api.getModuleLoader()

    def on_request_update(self, code: bytes, state: int):
        request = self.all_requests.get(code)
        assert request is not None, "Request can't be None."

        if state == self.state_error:
            request.receiver.socket.send_message(
                'FileTransfer',
                code=code,
                action=self.action_finish,
                state=self.state_error,
                reason=request.error_text
            )
        elif state in (self.state_cancelled, self.state_completed, self.state_timed_out_client_response,
                       self.state_clientDeclined,
                       self.state_serverDeclined):
            request.receiver.socket.send_message(
                'FileTransfer',
                code=code,
                action=self.action_finish,
                state=state,
                reason=request.error_text
            )
        elif state in (self.state_clientAccepted, self.state_serverAccepted):
            request.connect()
            # if isinstance(request, SelfReceiver):
            #     request.connect()
            # elif isinstance(request, SelfSender):

            # request.receiver.socket.send_message(
            #     'FileTransfer',
            #     code=code,
            #     action=self.action_update,
            #     state=self.state_sending
            # )
        elif state == self.state_sending:
            if isinstance(request, SelfReceiver):
                request.start_receiving()
            if isinstance(request, SelfSender):
                request.start_sending()
        else:
            print('out of if close', state)
            raise ValueError(f"Out of if clause: \ncode: {code}\nstate: {state}.")

    def checking_file_transfer_type(self, msg: dict):
        sender: Account = msg.get('_account')
        code = msg.get('code')
        files = msg.get('files')
        action = msg.get('action')
        state = msg.get('state')
        moduleID = msg.get('moduleId')
        receiver = msg.get('receiver')
        reason = msg.get('reason')

        # TODO: RECEIVER BECOMES LAGGY
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
                    self.receivingRequests[code] = request
                    request.updateState(self.state_clientAccepted, call_function=True, update_state=False)
                else:
                    self.sendDecline(code, sender.socket, "Unsupportable.")
                    return

                self.checking_requests()
                return

            request = self.all_requests.get(code)

            if action in (self.action_update, self.action_finish):
                # Checking for request existence
                if request is None:
                    self.sendError(code, sender.socket, "Request is not found.")
                    return
                if sender not in (request.receiver, request.sender, self.accountManager.getOwner()):
                    self.sendError(code, sender.socket, "You are not a participant of this request.")
                    return
            else:
                self.sendError(code, sender.socket, "Action is not registered.")
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
                if self.all_requests.get(request.code):
                    self.all_requests.pop(request.code)
                    self.receivingRequests.pop(request.code)
        except Exception as e:
            self.sendError(code, sender.socket, e.__str__())
            print(format_exc())
            return

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
