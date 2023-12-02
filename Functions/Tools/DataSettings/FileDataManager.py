from Functions.Tools.DataSettings.DataFile import DataFile


class DataManager:
    def __init__(self):
        self.settingDict: dict[str, DataFile] = {}

    def create(self, name: str, path: str):
        """Creates Datafile class with its name"""
        if self.settingDict.get(name) is not None:
            raise FileExistsError("File with this name is already created!")

        self.settingDict[name] = DataFile(path)

    def closeAll(self):
        """Saves data and closes files."""
        for file in self.settingDict.values():
            file.close()
        self.settingDict.clear()

    def close(self, name: str):
        """Saves data and closes file."""
        self.settingDict.pop(name).close()

    def get(self, name: str) -> DataFile:
        """Gets datafile object."""
        return self.settingDict.get(name)
