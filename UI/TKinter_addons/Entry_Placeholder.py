import tkinter as tk


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.disable_focus = False

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self._foc_in)
        self.bind("<FocusOut>", self._foc_out)

        self._put_placeholder()

    def _put_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

    def _foc_in(self, *args):
        if self.disable_focus:
            self.master.focus()
            self._foc_out()

        if self.cget('fg') == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def _foc_out(self, *args):
        if not self.get():
            self._put_placeholder()

    def change_placeholder_text(self, text):
        self._foc_in()
        self.placeholder = text
        self._foc_out()

    def disableFocus(self, mode: bool):
        self.disable_focus = mode
        if mode:
            self.master.focus()
            self._foc_out()
