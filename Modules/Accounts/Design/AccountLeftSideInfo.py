import random
import tkinter as tk

from Functions.Network.Accounts.AccountData import Account


class LeftSideInfo:
    nicknameFont = (None, 10, 'bold')
    pcFont = (None, 10, 'italic')
    pingFont = (None, 9, 'normal')

    def __init__(self, root: tk.Frame, account: Account):
        print('bruh')
        self.root = root
        self.account = account

        self.mainFrame = tk.Frame(root)

        self.nickname = tk.Label(self.mainFrame, font=self.nicknameFont, width=20)
        self.pc_name = tk.Label(self.mainFrame, font=self.pcFont, fg='#AFAFAF', width=20)
        self.ping = tk.Label(self.mainFrame, font=self.pingFont)

        self.mainFrame.pack(ipady=10, fill=tk.X)

        self.nickname.pack()
        self.pc_name.pack()
        self.ping.pack()

        # Bind the event handlers
        self.nickname.bind("<Enter>", self.on_enter)
        self.nickname.bind("<Leave>", self.on_leave)
        self.nickname.bind("<Button-1>", self.on_click)

        self.pc_name.bind("<Enter>", self.on_enter)
        self.pc_name.bind("<Leave>", self.on_leave)
        self.pc_name.bind("<Button-1>", self.on_click)

        self.ping.bind("<Enter>", self.on_enter)
        self.ping.bind("<Leave>", self.on_leave)
        self.ping.bind("<Button-1>", self.on_click)

        self.mainFrame.bind("<Enter>", self.on_enter)
        self.mainFrame.bind("<Leave>", self.on_leave)
        self.mainFrame.bind("<Button-1>", self.on_click)

        self.updateInfo()

    def updateInfo(self):
        self.nickname.configure(text=f'{self.account.nickname}')
        self.pc_name.configure(text=f'{self.account.pc_name}')
        if random.randint(1, 5) == 1:
            self.ping.configure(text=f'5000')
        else:
            self.ping.configure(text=f'Ping: {self.account.ping}')

    def on_enter(self, event):
        event.widget.config(cursor="hand2")

    def on_leave(self, event):
        event.widget.config(cursor="")

    def on_click(self, event):
        print(f"widget was clicked!")
