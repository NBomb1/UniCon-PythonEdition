import tkinter as tk
from threading import Thread
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from traceback import format_exc


class ChatText(ScrolledText):
    """Can be used also for logs, not only for the chat."""
    def __init__(self, master):
        super().__init__(master)
        # self.tag_configure("system-message", )

        self.tag_configure("g", foreground="green")
        self.tag_configure("nickname1", font=(None, 11, 'bold'))
        self.tag_configure("nickname2", foreground="green", font=(None, 11, 'bold'))
        self.tag_configure("nickname3", foreground="red", font=(None, 11, 'bold'))
        self.tag_configure("time", foreground="blue")

        self.configure(state=tk.DISABLED)
        self.bind("<F1>", self.save)
        # self.bind("<ButtonRelease-3>", self.options)

    def create_message(self, data: dict, time: datetime, scheme: str, colorscheme: dict, new_line=True, ) -> int:
        # preparation
        scroll = (self.yview()[1] == 1)
        self.configure(state=tk.NORMAL)
        # length of all text minus length of text without '\n'
        index = len(self.get('1.0', tk.END)) - len(self.get('1.0', tk.END).replace('\n', ''))

        # creating main default settings
        data['time'] = str(time.time())

        text = scheme + ('\n' if new_line else '')
        for i in data.keys():
            text = text.replace('{' + f'{i}' + '}', data.get(i))

        # inserting text to widget
        self.insert(tk.END, text)

        if colorscheme.get('time') is None and (scheme.find('{time}') != -1):
            colorscheme['time'] = 'time'

        # coloring
        for i in range(len(colorscheme)):
            try:
                self.tag_add(
                    tuple(colorscheme.values())[i],
                    f"{index}.{text.find(data.get(tuple(colorscheme.keys())[i]))}",
                    f"{index}."
                    f"{text.find(data.get(tuple(colorscheme.keys())[i])) + len(data.get(tuple(colorscheme.keys())[i]))}"
                )
            except TypeError as error:
                print(format_exc())
                print('data = ', data)
                print(list(colorscheme.keys())[i])
                raise error

        # disabling user changing
        self.configure(state=tk.DISABLED)
        # going down if the user in the end of a text
        if scroll:
            self.see(tk.END)
        return len(text)

    def save(self, event=None):
        filePath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"Text widget",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save text as"
        )
        if not filePath:
            return

        def func(path, logs):
            with open(path, mode='w', encoding='utf-8') as file:
                file.write(logs)
            self.create_message(
                {
                    'text':"The text has been saved. Path: ",
                    "path": filePath,
                    'name': 'Text_Chat'
                },
                datetime.now(),
                '[{name}]: {text}{path}',
                {
                    'path': 'nickname1',
                    'name': 'time'
                }
            )

        Thread(target=func, args=(filePath, self.get('0.0', tk.END))).start()

    # TODO: May be used in future updates

    # def options(self, event: tk.Event):
    #     temp = tk.Toplevel(self.master)
    #     temp.wm_overrideredirect(True)
    #     temp.focus_force()
    #     button = tk.Button(temp, text='Copy', command=lambda: temp.destroy())
    #     button.pack(ipadx=15)
    #     temp.update_idletasks()
    #     temp.geometry(f"{temp.winfo_width()}x{temp.winfo_height()}+{event.x_root}+{event.y_root}")
    #     temp.bind('<FocusOut>', lambda x: temp.destroy())
