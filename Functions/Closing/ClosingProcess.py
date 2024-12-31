from traceback import print_exc

from Functions.Closing.BeforeClose import beforeClose
from UI.MainMenu import MainMenu
from tkinter import messagebox


def closing(mainMenu: MainMenu, askBeforeClosing=True):
    if (
            askBeforeClosing and
            (mainMenu.server is not None or mainMenu.client is not None)
            and not
    messagebox.askokcancel("Confirmation", "Are you sure want to close program while in progress?")
    ):
        return
    try:
        mainMenu.logs.sendAll('[UniCon] Closing application...')
        beforeClose(mainMenu.dataManager, mainMenu, askBeforeClosing)
    except Exception:
        print_exc()
    mainMenu.root.destroy()
