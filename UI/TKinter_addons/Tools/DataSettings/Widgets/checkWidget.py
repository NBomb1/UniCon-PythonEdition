import tkinter as tk

from UI.TKinter_addons.Tools.DataSettings.Widgets.Basic.SaveWidgetData import SaveWidgetData


class CheckButton(tk.Checkbutton, SaveWidgetData):
    def __init__(self, widget: tk.Widget, text: str, default=False, onSave: callable = None, onClick=None):
        self.onSave: callable = onSave
        super().__init__(widget, text=text)
        self.v = tk.BooleanVar(self, default)
        self.configure(variable=self.v)
        self.savedData = default
        self.onClick = onClick
        if onClick:
            self.bind('<ButtonRelease>', lambda x: self.after(0, self.trigger))  # Bind to left-click event

        self._loadFunc(self._load)
        self._previous_data = self.v.get()

    def trigger(self):
        if self._previous_data == self.v.get():
            return
        # focusing on the root. It doesn't fix all problems, so it will be deleted soon
        self.tk.call('focus', '.')
        self.update()

        self._previous_data = self.v.get()
        self.onClick()

    def _load(self, data):
        self.v.set(data)
        self.savedData = data

    def save(self) -> bool:
        if self.onSave is not None:
            self.onSave(self)
        self.dataSaver(self.v.get())
        self.savedData = self.v.get()
        return self.v.get()
