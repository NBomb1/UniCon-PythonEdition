from traceback import print_exc

from Functions.Closing.AfterClose import afterClose
from UI.MainMenu import MainMenu
from tkinter import messagebox


def closing(mainMenu: MainMenu):
    if (
            (mainMenu.server is not None or mainMenu.client is not None)
            and not
            messagebox.askokcancel("Confirmation", "Are you sure want to close program while in progress?")
    ):
        return

    try:
        afterClose(mainMenu.dataManager, mainMenu)
    except Exception:
        print_exc()
    mainMenu.root.destroy()
