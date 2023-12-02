import tkinter as tk
from threading import Thread
from time import sleep

import settings


class ShowRedFlag:
    @staticmethod
    def showFlag(
            widget: tk.Widget,
            bgAfterChange='#FF2B2A',
            fgAfterChange='white',
    ):
        ShowRedFlag.disableFocus(widget, True)
        bgOrigin = widget.cget('bg')
        fgOrigin = widget.cget('fg')

        widget.configure(bg=bgAfterChange)
        widget.configure(fg=fgAfterChange)

        def func():
            sleep(settings.SettingsMenu.widgetsWait)
            widget.configure(bg=bgOrigin)
            widget.configure(fg=fgOrigin)
            ShowRedFlag.disableFocus(widget, False)

        Thread(target=func, daemon=True).start()

    @staticmethod
    def disableFocus(widget: tk.Widget, mode: bool):
        func = getattr(widget, 'disableFocus')
        if func is not None:
            func(mode)
