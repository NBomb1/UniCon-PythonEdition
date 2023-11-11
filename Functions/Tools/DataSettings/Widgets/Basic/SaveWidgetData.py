from functools import partial

from Functions.Tools.DataSettings.DataFile import DataFile


class SaveWidgetData:
    dataSaver: callable = None

    def connect(self, datafile: DataFile, name: str):
        self.dataSaver = partial(datafile.put, name)
