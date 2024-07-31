import tkinter as tk


class EntryWithPlaceholder(tk.Entry):
    emptySymbols = '‎ ‎ ‎ '

    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.disable_focus = False

        self.placeholder = placeholder + self.emptySymbols
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self._foc_in)
        self.bind("<FocusOut>", self._foc_out)
        self.show = None
        self.isPressingKey = False

        self._put_placeholder()

        # Bind F1 key press event
        self.bind("<F1>", self.show_symbols)
        self.bind("<KeyRelease-F1>", self.keyRelease)

    def _put_placeholder(self):
        if not len(self.get()) and self.cget('fg') != 'white':
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color
            self.configure(show='')
        else:
            self.configure(show=self.show)

    def _foc_in(self, *args):
        if self.disable_focus:
            self.master.focus()
            self._foc_out()

        if self.cget('fg') == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            self.configure(show=self.show)

    def _foc_out(self, *args):
        self._put_placeholder()

    def change_placeholder_text(self, text):
        self._foc_in()
        self.placeholder = text
        self._foc_out()

    def disableFocus(self, mode: bool):
        self.disable_focus = mode
        if mode:
            self._foc_out()
        else:
            self._foc_in()

    def get(self) -> str:
        return super().get() if self.placeholder != super().get() else ''

    def put(self, text: str):
        if not text:
            return
        self._foc_in()
        self.delete(0, tk.END)
        self.insert(0, text)

    def hideInfo(self, show='*'):
        self.show = show

    def showInfo(self):
        self.show = None

    def show_symbols(self, event):
        if self.show is None:
            return
        if not self.cget('show') and not self.isPressingKey:
            self.configure(show=self.show)

        elif self.focus_get() == self:
            self.configure(show='')
            self.isPressingKey = True

    def keyRelease(self, event):
        if self.show:
            self.isPressingKey = False
            self.show_symbols(event)
