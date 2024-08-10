import tkinter as tk
from tkinter import simpledialog, messagebox
from functools import partial

from Functions.ModuleHandler.moduleAPI import API
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Network.DataTransfer import MessageTransfer


class RightSideInfo:
    api: API
    accountManager: AccountManager
    frameMainInfo = None
    current: Account = None
    accountId: tk.Label = None
    accountPcName: tk.Label = None
    accountPing: tk.Label = None
    accountName: tk.Label = None
    accountTags: tk.Label = None
    accountCons: tk.Label = None
    accountIdLabel: tk.Label = None
    accountPcNameLabel: tk.Label = None
    accountPingLabel: tk.Label = None
    accountNameLabel: tk.Label = None
    accountTagsLabel: tk.Label = None
    accountConsLabel: tk.Label = None
    accountKickButton: tk.Button = None
    accountKickReasonButton: tk.Button = None
    font = (None, 13)
    isShowing = False

    def createWidgets(self, root: tk.Widget):
        self.frameMainInfo = tk.Frame(root)
        self.frameMainInfo.pack(fill=tk.X)
        self.frameMainInfo.grid_columnconfigure(1, weight=True)
        self.frameMainInfo.grid_rowconfigure(1, pad=5)
        self.frameMainInfo.grid_rowconfigure(3, pad=5)
        self.frameMainInfo.grid_rowconfigure(5, pad=5)
        self.frameMainInfo.grid_rowconfigure(6, weight=True)

        self.accountNameLabel = tk.Label(self.frameMainInfo, text='Nickname:', font=self.font)
        self.accountPingLabel = tk.Label(self.frameMainInfo, text='Ping:', font=self.font)
        self.accountPcNameLabel = tk.Label(self.frameMainInfo, text='PC name:', font=self.font)
        self.accountIdLabel = tk.Label(self.frameMainInfo, text='ID:', font=self.font)
        self.accountTagsLabel = tk.Label(self.frameMainInfo, text='Tags:', font=self.font)
        self.accountConsLabel = tk.Label(self.frameMainInfo, text='E. Conns.:', font=self.font)

        self.accountName = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E)
        self.accountPing = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E)
        self.accountPcName = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E)
        self.accountId = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E)
        self.accountTags = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E)
        self.accountCons = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E, justify=tk.RIGHT)

        self.accountKickButton = tk.Button(self.frameMainInfo, text='Kick', state=tk.DISABLED)
        self.accountKickReasonButton = tk.Button(self.frameMainInfo, text='Kick with Reason', state=tk.DISABLED)

    def updateName(self, name: str):
        self.accountName.configure(text=name)

    def updatePing(self, ping: str | int):
        self.accountPing.configure(text=str(ping))

    def updateTags(self, tags: list):
        text = f", ".join(tags) + f' - [{len(tags)}]'
        self.accountTags.configure(text=text if tags else 'None')

    def updateConnections(self, obj: dict[str, list[MessageTransfer]]):
        text = ''
        for i in obj:
            text += self.api.getModuleHandler().findById(i).name + f' - {len(obj[i])}\n'
        self.accountCons.configure(text=text.rstrip('\n') if text else 'None')

    def triggeredUpdate(self, account: Account, what: str):
        if account != self.current and what != '':
            return
        self.updatePing(account.ping)
        self.updateName(account.nickname)
        self.updateTags(account.tags)
        self.updateConnections(account.extraConnections)
        if self.api.getAccountManager().getIsServer():
            if account in self.api.getAccountManager().getParticipants():
                self.accountKickButton.configure(
                    state=tk.NORMAL,
                    command=partial(self.kickAccount, account, False),
                    text='Kick'
                )
                self.accountKickReasonButton.configure(state=tk.NORMAL,
                                                       text='Kick with Reason',
                                                       command=partial(
                                                           self.kickAccount,
                                                           account,
                                                           True
                                                       )
                                                       )
            elif isinstance(account, SelfAccount):
                self.accountKickReasonButton.configure(text='Kick all with a reason',
                                                       command=(lambda: self.kickAll(True)),
                                                       state=tk.NORMAL
                                                       if self.accountManager.getParticipants()
                                                       else tk.DISABLED
                                                       )
                self.accountKickButton.configure(text='Kick all',
                                                 command=(lambda: self.kickAll),
                                                 state=tk.NORMAL if self.accountManager.getParticipants()
                                                 else tk.DISABLED
                                                 )
        else:
            self.accountKickReasonButton.configure(state=tk.DISABLED)
            self.accountKickButton.configure(state=tk.DISABLED)

    def show(self, account: Account):
        if self.current == account:
            try:
                self.frameMainInfo.pack_info()
                self.frameMainInfo.pack_forget()
            except tk.TclError:
                self.frameMainInfo.pack(fill=tk.X)
            return
        self.frameMainInfo.pack(fill=tk.X)

        account.addUpdatedAccount(self.triggeredUpdate)
        if self.current is not None:
            self.current.removeUpdatedAccount(self.triggeredUpdate)
        self.accountPcName.configure(text=account.pc_name)
        self.accountId.configure(text=f'{account.id}')
        self.triggeredUpdate(account, '')

        self.current = account

        if self.isShowing:
            return
        self.isShowing = True
        self.accountNameLabel.grid(column=0, row=0, sticky=tk.W)
        self.accountPingLabel.grid(column=0, row=1, sticky=tk.W)
        self.accountPcNameLabel.grid(column=0, row=2, sticky=tk.W)
        self.accountIdLabel.grid(column=0, row=3, sticky=tk.W)
        self.accountTagsLabel.grid(column=0, row=4, sticky=tk.W)
        self.accountConsLabel.grid(column=0, row=5, sticky=tk.W)

        self.accountName.grid(column=1, row=0, sticky=tk.E)
        self.accountPing.grid(column=1, row=1, sticky=tk.E)
        self.accountPcName.grid(column=1, row=2, sticky=tk.E)
        self.accountId.grid(column=1, row=3, sticky=tk.E)
        self.accountTags.grid(column=1, row=4, sticky=tk.E)
        self.accountCons.grid(column=1, row=5, sticky=tk.E)
        self.accountKickButton.grid(column=0, row=6, sticky=tk.NSEW, columnspan=2)
        self.accountKickReasonButton.grid(column=0, row=7, sticky=tk.NSEW, columnspan=2)

    def kickAccount(self, account: Account, askReason: bool = False, text=None):
        reason = 'You were kicked by the server.' if text is None else text
        if askReason:
            reason = simpledialog.askstring('Kick Reason', 'Enter a reason for kicking: ')
            if reason is None:
                return
        self.api.getAccountManager().kickAccount(
            self.api.getAccountManager().getSelfAccount(),
            account,
            reason
        )
        self.accountKickButton.configure(state=tk.DISABLED)
        self.accountKickReasonButton.configure(state=tk.DISABLED)

    def kickAll(self, askReason: bool = False):
        if not messagebox.askyesno('WARNING', 'Do really you want to kick all accounts?'):
            return

        reason = None
        if askReason:
            reason = simpledialog.askstring('Kick Reason', 'Enter a reason for kicking all players: ')
            if reason is None:
                return

        for account in self.api.getAccountManager().getParticipants():
            self.kickAccount(account, False, reason)
