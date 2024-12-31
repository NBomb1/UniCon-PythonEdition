from os import getcwd
from sys import version_info
import tkinter as tk

from UI.window.WindowCenter import center_main


class VersionChecker:
    """
    A class to display a warning message when the Python version is not recommended.

    Attributes:
    pythonVersion (str): The current Python version.
    text (str): The warning message text.
    textFont (tuple): The font style for the warning message.
    buttonFont (tuple): The font style for the buttons.

    Methods:
    __init__(): Initializes the GUI window and displays the warning message and buttons.
    """
    pythonVersion = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    text = f'You are using python {pythonVersion}\n' \
           f'which is not recommended to run this app.\n' \
           f'Program is incompatible with versions below 3.10.'
    textFont = (None, 15, 'bold')
    buttonFont = (None, 10, 'bold')

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Incompatible python version!')
        self.root.geometry('550x200')
        self.root.wm_resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", exit)

        center_main(self.root)

        self.inactiveImage = tk.PhotoImage(file=getcwd() + r'\UI\NoConnection.gif')
        self.root.wm_iconphoto(False, self.inactiveImage)

        self.label = tk.Label(self.root, text=self.text, font=self.textFont)
        self.buttonContinue = tk.Button(self.root, text='Continue anyway', command=self.root.destroy,
                                        font=self.buttonFont)
        self.buttonClose = tk.Button(self.root, text='Close the app', command=exit, font=self.buttonFont)

        self.label.pack(fill=tk.BOTH, anchor=tk.CENTER, expand=True)
        self.buttonContinue.pack(side=tk.LEFT, expand=True, fill=tk.X, anchor=tk.S)
        self.buttonClose.pack(side=tk.RIGHT, expand=True, fill=tk.X, anchor=tk.S)

        self.root.mainloop()


def start():
    if version_info.major == 3 and version_info.minor >= 10:
        return
    VersionChecker()
