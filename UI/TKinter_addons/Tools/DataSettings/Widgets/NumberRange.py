import tkinter as tk

from Functions.Checks import checkInteger
from UI.TKinter_addons.Tools.DataSettings.Widgets.Basic.NumberRangeSpinbox import NumberRangeBasic
from UI.TKinter_addons.Tools.DataSettings.Widgets.Basic.SaveWidgetData import SaveWidgetData
from UI.TKinter_addons.Tools.DataSettings.Widgets.Basic.ShowRedFlag import ShowRedFlag
from UI.TKinter_addons.Tools.DataSettings.Widgets.Basic.ToolTip import ToolTip


class NumberRange(tk.LabelFrame, SaveWidgetData, ShowRedFlag):
    def __init__(
            self,
            master: tk.Widget,
            labelText: str,
            minFrom: int,
            maxFrom: int,
            minTo: int,
            maxTo: int,
            startNumberFrom: int,
            startNumberTo: int,
            numberExceptionBoth: list[int] = None,
            numberExceptionFrom: list[int] = None,
            numberExceptionTo: list[int] = None,
            checkFuncBoth: list[callable] = None,
            checkFuncFrom: list[callable] = None,
            checkFuncTo: list[callable] = None,
    ):
        self.disable_focus = False

        numberExceptionFrom = [] if numberExceptionFrom is None else numberExceptionFrom
        numberExceptionTo = [] if numberExceptionTo is None else numberExceptionTo
        numberExceptionBoth = [] if numberExceptionBoth is None else numberExceptionBoth
        checkFuncFrom = [] if checkFuncFrom is None else checkFuncFrom
        checkFuncBoth = [] if checkFuncBoth is None else checkFuncBoth
        checkFuncTo = [] if checkFuncTo is None else checkFuncTo

        super().__init__(master, text=labelText)

        self.actualData: list[int, int] = [minFrom, maxTo]
        self.minFrom: int = minFrom
        self.minTo: int = minTo
        self.maxFrom: int = maxFrom
        self.maxTo: int = maxTo
        self.startNumberFrom: int = startNumberFrom
        self.startNumberTo: int = startNumberTo

        self.checkFuncFrom = checkFuncFrom
        self.checkFuncTo = checkFuncTo
        self.checkFuncFrom.extend(checkFuncBoth)
        self.checkFuncTo.extend(checkFuncBoth)

        self.numberExceptionFrom = numberExceptionFrom
        self.numberExceptionTo = numberExceptionTo
        self.numberExceptionFrom.extend(numberExceptionBoth)
        self.numberExceptionTo.extend(numberExceptionBoth)

        self.pastValueFrom = startNumberFrom
        self.pastValueTo = startNumberTo

        self.From = NumberRangeBasic(self, self.minFrom, self.maxFrom,
                                     self.startNumberFrom, self.numberExceptionFrom,
                                     self.checkFuncFrom
                                     )
        self.LabelFrom = tk.Label(self, text='From')

        self.To = NumberRangeBasic(self, self.minTo, self.maxTo,
                                   self.startNumberTo, self.numberExceptionTo,
                                   self.checkFuncTo
                                   )
        self.LabelTo = tk.Label(self, text='To')

        self.ToolTipFrom = ToolTip(self.From, '')
        self.ToolTipTo = ToolTip(self.To, '')

        self.LabelFrom.pack()
        self.From.pack()
        self.LabelTo.pack()
        self.To.pack()
        self._loadFunc(self.load)

    def load(self, data: list[str, str]):
        DataFrom_, DataTo = data
        self.From.load(DataFrom_)
        self.To.load(DataTo)

    def save(self) -> list[list[str], list[str]]:
        """
        :return: list of refuse reasons.
        """
        res = self.checkCorrectness()
        if not len(res[0]) and not len(res[1]):
            self.actualData = [self.From.actualData, self.To.actualData]
            if self.dataSaver is not None:
                self.dataSaver(self.actualData)
        else:
            self.bell()
        self.showResults(res)
        return res

    def checkCorrectness(self) -> list[list[str], list[str]]:
        errors_from: list[str] = []
        errors_to: list[str] = []

        if not checkInteger(self.From.get()):
            errors_from.append("Isn't number")
        if not checkInteger(self.To.get()):
            errors_to.append("Isn't number")

        if not errors_from and not errors_to and int(self.From.get()) > int(self.To.get()):
            errors_from.append("Incorrect range")
            errors_to.append("Incorrect range")

        if not errors_from and not errors_to:
            errors_from.extend(self.From.save())
            errors_to.extend(self.To.save())

        return [errors_from, errors_to]

    def showResults(self, results: list[list[str], list[str]]):
        from_, to = results
        from_ = '\n'.join(from_)
        to = '\n'.join(to)

        if from_:
            self.showFlag(self.From)
        if to:
            self.showFlag(self.To)

        self.ToolTipFrom.change_text(from_)
        self.ToolTipTo.change_text(to)

    def disableFocus(self, mode: bool):
        self.disable_focus = mode
        self.From.disableFocus(mode)
        self.To.disableFocus(mode)
