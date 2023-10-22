import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime


class ChatText(ScrolledText):
    """Can be used also for logs, not only for the chat."""
    def __init__(self, master):
        super().__init__(master)
        self.tag_configure("system-message", background="green", foreground='white')
        self.tag_configure("username", foreground="green")
        self.tag_configure("time", foreground="blue")
        self.tag_configure("message", foreground="red")
        self.configure(state=tk.DISABLED)

    def create_message(self, data: dict, time: datetime, scheme: str, colorscheme: dict, new_line=True):
        # preparation
        scroll = (self.yview()[1] == 1)
        self.configure(state=tk.NORMAL)
        # length of all text minus length of text without '\n'
        index = len(self.get('1.0', tk.END)) - len(self.get('1.0', tk.END).replace('\n', ''))

        # baking text
        time = f"{'' if len(str(time.hour)) == 2 else '0'}{time.hour}:" \
               f"{'' if len(str(time.minute)) == 2 else '0'}{time.minute}:" \
               f"{'' if len(str(time.second)) == 2 else '0'}{time.second}"
        text = scheme + ('\n' if new_line else '')
        for i in data.keys():
            text = text.replace('{' + f'{i}' + '}', data.get(i))

        # inserting text to widget
        self.insert(tk.END, text)

        # creating main default settings
        data['time'] = time

        if colorscheme.get('time') is None and (scheme.find('{time}') != -1):
            colorscheme['time'] = 'time'

        # coloring
        for i in range(len(colorscheme)):
            try:
                self.tag_add(
                    list(colorscheme.values())[i],
                    f"{index}.{text.find(data.get(list(colorscheme.keys())[i])) }",
                    f"{index}."
                    f"{text.find(data.get(list(colorscheme.keys())[i])) + len(data.get(list(colorscheme.keys())[i]))}"
                )
            except TypeError as error:
                print(error)
                print('data = ', data)
                print(list(colorscheme.keys())[i])

        # disabling user changing
        self.configure(state=tk.DISABLED)
        # going down if the user in the end of a text
        if scroll:
            self.yview_scroll(111, 'units')
