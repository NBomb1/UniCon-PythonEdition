import tkinter as tk

from Functions.Tools.DataSettings.Widgets.Basic.SaveWidgetData import SaveWidgetData


class CheckButton(tk.Checkbutton, SaveWidgetData):
    def __init__(self, widget: tk.Widget, text: str, default=False, onSave: callable = None):
        self.onSave: callable = onSave
        super().__init__(widget, text=text)
        self.v = tk.BooleanVar(self, default)
        self.configure(variable=self.v)

        self._loadFunc(self._load)

    def _load(self, data):
        self.v.set(data)

    def save(self) -> bool:
        if self.onSave is not None:
            self.onSave(self)
        self.dataSaver(self.v.get())
        return self.v.get()
