"""
This module lets you chat with all participants.
"""
from datetime import datetime, timezone

from Functions.ModuleHandler.moduleAPI import API
import tkinter as tk

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.MainChannel.Server.main import ServerMainChannel
from Functions.Network.ModuleConnector.Client.InviteConnectionInfo import InviteConnectionInfo
from Functions.Network.ModuleConnector.WaitingForConnectionInfo import WaitingForConnectionInfo
from Modules.Chat.Client import Client
from Modules.Chat.Server import Server
from UI.TKinter_addons.Entry_Placeholder import EntryWithPlaceholder
from UI.TKinter_addons.Text_chat import ChatText


class Module:
    id_ = "GyUB7vkoB@7Vdv14dA%QLYs4kwmS99FygnTGSxo3CDIjR2r2IS06aBb6ZBmZIFl5"
    version = "0.0.1"
    name = "Chat"
    author = "ArT"
    defaultNetworkAuth = True
    isUI = True
    font = (None, 11, "normal")

    entry_message: tk.Entry = None
    text_chat: ChatText = None
    button_send: tk.Button = None

    def __init__(self, api: API):
        self.api = api
        self.logs = api.getLogs()
        self.server: Server | None = None
        self.client: Client | None = None
        self.notebook = self.api.getRightNotebook()
        self.triggerManager = self.api.getTriggerManager()

        self.frame = tk.Frame(self.api.getRightNotebook())
        self.notebook.add(self.frame, text='Chat', state=tk.DISABLED)
        self.notebook.tab(self.frame, state=tk.NORMAL)
        self.mcm = self.api.getConnectorManager()
        self.setup()

        self.api.getTriggerManager().serverStartedTrigger(self.startedAsServer)
        self.api.getAccountManager().clientStoppedTrigger(self.startedAsClientDisconnected)
        self.entry_message.bind("<Return>", self.onPressedEnter)

    def startedAsServer(self, obj: ServerMainChannel):
        self.server = Server(self.api, self)
        self.api.getTriggerManager().accountAddedTrigger(self.inviteAccount)
        self.api.getAccountManager().serverStoppedTrigger(self.startedAsServerClosed)
        self.unlockChat()

    def startedAsServerClosed(self):
        self.api.getAccountManager().serverStoppedTriggerREMOVE(self.startedAsServerClosed)
        self.lockChat()
        self.server.stop()
        self.server = None

    def startedAsClientDisconnected(self):
        self.lockChat()
        self.client = None

    def unlockChat(self):
        self.entry_message.configure(state=tk.NORMAL)
        self.button_send.configure(state=tk.NORMAL)

    def lockChat(self):
        self.entry_message.configure(state=tk.DISABLED)
        self.button_send.configure(state=tk.DISABLED)

    def setTypes(self, msg: MessageTransfer):
        msg.registerType('chat')
        msg.registerType('close')
        msg.registerType('sys')

    def inviteAccount(self, account: Account):
        """Server function"""
        WaitingForConnectionInfo(
            self.id_,
            self.api.getConnectorManager().server.addConnectionWaiting,
            account,
            self.clientConnected,
            15,
            self.clientDeclined
        )

    def setup(self):
        # Creating chat widgets
        self.button_send = tk.Button(self.frame, text='Send', command=self.sendMessage)
        self.text_chat = ChatText(self.frame)
        self.text_chat.configure(wrap=tk.WORD, height=20, font=self.font)
        self.entry_message = EntryWithPlaceholder(
            self.frame,
            'Type your message...'
        )

        # Placing widgets
        self.text_chat.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.N, expand=True)
        self.entry_message.pack(side=tk.LEFT, anchor=tk.N, fill=tk.X, expand=tk.YES, ipady=3, pady=(4, 3))
        self.button_send.pack(ipadx=10, pady=(4, 3))
        self.log('This is the start of chat.')
        # setting by defaults
        self.entry_message.configure(state=tk.DISABLED)
        self.button_send.configure(state=tk.DISABLED)

    def log(self, message: str, time: datetime | None = None):
        self.text_chat.create_message(
            {
                'message': message
            },
            time if time is not None else datetime.now().replace(microsecond=0),
            '<{time}> {message}',
            {
                'message': 'system-message'
            }
        )

    def message_(self, message: str, nickname: str, time: datetime, markGreen=False):
        mark = '2' if markGreen else '1'
        self.text_chat.create_message(
            {
                'message': message,
                'nickname': nickname
            },
            time,
            '<{time}-{nickname}> {message}',
            {
                'message': 'system-message',
                'nickname': 'nickname' + mark
            }
        )

    def messageID(self, message: str, id: str, time: datetime, markGreen=False):
        mark = '2' if markGreen else '1'
        self.text_chat.create_message(
            {
                'message': message,
                'id': id
            },
            time,
            '<{time}-id-{id}> {message}',
            {
                'message': 'system-message',
                'id': 'nickname' + mark
            }
        )

    def clientConnected(self, obj: WaitingForConnectionInfo):
        """ServerSide: Client connected to server."""
        self.logs.sendLog('[Chat] Client connected.', -1)
        self.setTypes(obj.socket)
        self.server.add(obj.socket)

    def clientDeclined(self, obj: WaitingForConnectionInfo):
        """ServerSide: Client declined server invite."""
        self.api.getLogs().sendLog("Client declined chat connection invite.", -1)

    def mcm_inviteConnection(self, invite: InviteConnectionInfo):
        """ClientSide: Client accepted server invite."""
        self.logs.sendLog('[Chat] Accepting the invite...', -1)
        s: MessageTransfer = invite.accept()
        self.setTypes(s)
        self.client = Client(self.api, self, s)
        self.unlockChat()

    def sendMessage(self):
        message = self.entry_message.get()
        if not message:
            return
        self.entry_message.delete(0, tk.END)
        self.button_send.configure(state=tk.DISABLED)
        self.button_send.after(500, lambda: self.button_send.configure(state=tk.NORMAL))
        if self.server:
            self.server.sendMessage(message, 'chat')
        if self.client:
            self.client.sendMessage(message, 'chat')

    def onPressedEnter(self, event):
        if self.button_send.cget("state") == tk.NORMAL:
            self.sendMessage()
