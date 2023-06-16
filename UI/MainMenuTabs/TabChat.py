import tkinter as tk
from UI.TKinter_addons.Entry_Placeholder import EntryWithPlaceholder
from UI.TKinter_addons.Text_chat import ChatText
from datetime import datetime


class TabChat(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Creating chat widgets
        self.chat_button_send = tk.Button(self, text='send')
        self.chat_text = ChatText(self)
        self.chat_text.configure(wrap=tk.WORD, height=20)
        self.chat_entry_message = EntryWithPlaceholder(
            self,
            'Type your message...'
        )

        # Placing widgets
        self.chat_text.pack(fill=tk.X, side=tk.TOP, anchor=tk.N)
        self.chat_entry_message.pack(side=tk.LEFT, anchor=tk.N, fill=tk.X, expand=tk.YES, ipady=3, pady=(4, 0))
        self.chat_button_send.pack(ipadx=10, pady=(4, 0))

        self.chat_text.create_message(
            {
                'system': 'system',
                'message': 'Chat is loaded successfully!'
             },
            datetime.now(),
            '<{system}> {message}',
            {
                'system': 'username',
                'message': 'system-message'
            }
        )

        # setting by defaults
        self.chat_entry_message.configure(state=tk.DISABLED)
        self.chat_button_send.configure(state=tk.DISABLED)
