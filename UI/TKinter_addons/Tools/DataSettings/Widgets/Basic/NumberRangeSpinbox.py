from UI.TKinter_addons.Tools.DataSettings.Widgets.Basic.SaveWidgetData import SaveWidgetData
import tkinter as tk

from UI.TKinter_addons.Tools.DataSettings.Widgets.Basic.ShowRedFlag import ShowRedFlag
from UI.TKinter_addons.Tools.DataSettings.Widgets.Basic.ToolTip import ToolTip


class NumberRangeBasic(SaveWidgetData, tk.Spinbox, ToolTip, ShowRedFlag):
    def __init__(self,
                 master: tk.Widget,
                 from_: int,
                 to: int,
                 startValue: int,
                 numberException: list[int] = None,
                 checkFunc: list[callable] = None,
                 ):
        self.disable_focus = False

        numberException = [] if numberException is None else numberException
        checkFunc = [] if checkFunc is None else checkFunc

        self.master = master
        self.from_ = from_
        self.to_ = to
        self.actualData = startValue
        self.numberException = numberException
        self.checkFunc = checkFunc

        super().__init__(master)
        self.ToolTip = ToolTip(self, '')
        self._var = tk.StringVar(value=str(startValue))
        self.configure(textvariable=self._var, from_=from_, to=to)

        self.bind("<FocusIn>", self._foc_in)

    def load(self, data: str):
        self.actualData = data
        self.delete("0", tk.END)
        self.insert("1", str(data))

    def save(self) -> list[str]:
        """
        :return: list of refuse reasons.
        """
        res = self.checkCorrectness()
        if not len(res):
            self.actualData = self._var.get()
            if self.dataSaver is not None:
                self.dataSaver(self.actualData)
            self.showFlag(self, 'green')
        else:
            self.showFlag(self)
            self.bell()
        self.ToolTip.change_text('\n'.join(res))
        return res

    def checkCorrectness(self) -> list[str]:
        checkAll = [
            self.exceptionCheck,
            self.rangeCheck
        ]
        checkAll.extend(self.checkFunc)

        num = int(self._var.get())
        for i in range(len(checkAll)):
            checkAll[i] = checkAll[i](num)
        checkAll = list(filter(lambda x: x != '', checkAll))
        return checkAll

    def rangeCheck(self, number: int):
        return '' if self.from_ <= number <= self.to_ else f'Number {number} is out of range ({self.from_}:{self.to_}).'

    def exceptionCheck(self, number: int):
        return 'This value is in exception list.' if number in self.numberException else ''

    def disableFocus(self, mode: bool):
        self.disable_focus = mode
        if mode:
            self.master.focus()

    def _foc_in(self, *args):
        if self.disable_focus:
            self.master.focus()
