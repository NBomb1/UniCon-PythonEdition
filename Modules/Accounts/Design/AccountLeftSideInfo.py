import tkinter as tk

from Functions.Network.Accounts.AccountData import Account


class LeftSideInfo:
    nicknameFont = (None, 10, 'bold')
    pcFont = (None, 10, 'italic')

    def __init__(self, root: tk.Frame, account: Account):
        print('bruh')
        self.root = root
        self.account = account

        self.mainFrame = tk.Frame(root)

        self.nickname = tk.Label(self.mainFrame, font=self.nicknameFont)
        self.pc_name = tk.Label(self.mainFrame, font=self.pcFont, fg='#AFAFAF')
        self.ping = tk.Label(self.mainFrame)

        self.mainFrame.pack(ipady=10)

        self.nickname.grid(row=0, column=0, sticky=tk.W)
        self.pc_name.grid(row=1, column=0, sticky=tk.W)
        self.ping.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)

        self.updateInfo()

    def updateInfo(self):
        self.nickname.configure(text=f'{self.account.nickname}')
        self.pc_name.configure(text=f'{self.account.pc_name}')
        self.ping.configure(text=f'{self.account.ping}')
