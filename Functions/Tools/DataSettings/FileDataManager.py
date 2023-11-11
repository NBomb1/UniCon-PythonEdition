from Functions.Tools.DataSettings.DataFile import DataFile


class DataManager:
    def __init__(self):
        self.settingDict: dict[str, DataFile] = {}

    def create(self, name: str, path: str):
        self.settingDict[name] = DataFile(path)

    def closeAll(self):
        for file in self.settingDict.values():
            file.close()
        self.settingDict.clear()

    def close(self, name: str):
        self.settingDict[name].close()
        self.settingDict.pop(name)

    def get(self, name: str) -> DataFile:
        return self.settingDict.get(name)
