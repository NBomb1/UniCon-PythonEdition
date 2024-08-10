from functools import partial

from Functions.DataFile import DataFile


class SaveWidgetData:
    loadFunction: callable = None
    dataSaver: callable = None
    dataLoader: callable = None

    def connect(self, datafile: DataFile, name: str):
        self.dataSaver = partial(datafile.put, name)
        self.dataLoader = partial(datafile.get, name)
        if self.loadFunction is not None and self.dataLoader() is not None:
            self.loadFunction(self.dataLoader())

    def _loadFunc(self, loadFunction: callable):
        self.loadFunction = loadFunction
