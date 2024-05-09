import tkinter as tk

from Functions.Network.Accounts.AccountData import Account


class RightSideInfo:
    frameMainInfo = None
    current = None
    accountId = None
    accountPcName = None
    accountPing = None
    accountName = None
    accountTags = None
    accountIdLabel = None
    accountPcNameLabel = None
    accountPingLabel = None
    accountNameLabel = None
    accountTagsLabel = None
    font = (None, 13)

    def createWidgets(self, root: tk.Widget):
        self.frameMainInfo = tk.Frame(root)
        self.frameMainInfo.pack(fill=tk.X)
        self.frameMainInfo.grid_columnconfigure(1, weight=True)
        self.frameMainInfo.grid_rowconfigure(1, pad=10)
        self.frameMainInfo.grid_rowconfigure(3, pad=10)
        self.frameMainInfo.grid_rowconfigure(5, pad=10)

        self.accountNameLabel = tk.Label(self.frameMainInfo, text='Name:', font=self.font)
        self.accountPingLabel = tk.Label(self.frameMainInfo, text='Ping:', font=self.font)
        self.accountPcNameLabel = tk.Label(self.frameMainInfo, text='PC name:', font=self.font)
        self.accountIdLabel = tk.Label(self.frameMainInfo, text='ID:', font=self.font)
        self.accountTagsLabel = tk.Label(self.frameMainInfo, text='Tags:', font=self.font)

        self.accountName = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E)
        self.accountPing = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E)
        self.accountPcName = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E)
        self.accountId = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E)
        self.accountTags = tk.Label(self.frameMainInfo, font=self.font, anchor=tk.E)

    def updateName(self, name: str):
        self.accountName.configure(text=name)

    def updatePing(self, ping: str | int):
        self.accountPing.configure(text=str(ping))

    def triggeredPingUpdate(self, account: Account):
        if account != self.current:
            return
        self.updatePing(account.ping)

    def updateTags(self, tags: list):
        text = f", ".join(tags) + f' - [{len(tags)}]'
        self.accountTags.configure(text=text if tags else 'None')

    def show(self, account: Account):
        if self.current == account:
            return

        account.add_on_ping_update_function(self.triggeredPingUpdate)
        if self.current is not None:
            self.current.remove_on_ping_update_function(self.triggeredPingUpdate)
        self.accountPcName.configure(text=account.pc_name)
        self.accountId.configure(text=f'{account.id}')
        self.updateName(account.nickname)
        self.updatePing(account.ping)
        self.updateTags(account.tags)
        self.accountNameLabel.grid(column=0, row=0, sticky=tk.W)
        self.accountPingLabel.grid(column=0, row=1, sticky=tk.W)
        self.accountPcNameLabel.grid(column=0, row=2, sticky=tk.W)
        self.accountIdLabel.grid(column=0, row=3, sticky=tk.W)
        self.accountTagsLabel.grid(column=0, row=4, sticky=tk.W)

        self.accountName.grid(column=1, row=0, sticky=tk.E)
        self.accountPing.grid(column=1, row=1, sticky=tk.E)
        self.accountPcName.grid(column=1, row=2, sticky=tk.E)
        self.accountId.grid(column=1, row=3, sticky=tk.E)
        self.accountTags.grid(column=1, row=4, sticky=tk.E)
        self.current = account

    def checkCurrent(self, account: Account):
        return account == self.current
