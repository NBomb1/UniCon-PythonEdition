import tkinter as tk
from UI.TKinter_addons.Entry_Placeholder import EntryWithPlaceholder
from UI.TKinter_addons.Text_chat import ChatText
from datetime import datetime


class TabChat(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Creating chat widgets
        self.button_send = tk.Button(self, text='send')
        self.text_chat = ChatText(self)
        self.text_chat.configure(wrap=tk.WORD, height=20)
        self.entry_message = EntryWithPlaceholder(
            self,
            'Type your message...'
        )

        # Placing widgets
        self.text_chat.pack(fill=tk.X, side=tk.TOP, anchor=tk.N)
        self.entry_message.pack(side=tk.LEFT, anchor=tk.N, fill=tk.X, expand=tk.YES, ipady=3, pady=(4, 0))
        self.button_send.pack(ipadx=10, pady=(4, 0))

        self.text_chat.create_message(
            {
                'system': 'system',
                'message': 'Logs has been loaded successfully!'
             },
            datetime.now(),
            '<{system}> {message}',
            {
                'system': 'username',
                'message': 'system-message'
            }
        )

        # setting by defaults
        self.entry_message.configure(state=tk.DISABLED)
        self.button_send.configure(state=tk.DISABLED)
