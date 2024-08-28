from Functions.DataFile import DataFile


class FileDataManager:
    def __init__(self):
        self.settingDict: dict[str, DataFile] = {}

    def create(self, name: str, path: str):
        """Creates Datafile class with its name"""
        if self.settingDict.get(name) is not None:
            raise FileExistsError("File with this name is already created!")

        self.settingDict[name] = DataFile(path)

    def saveAll(self):
        """Saves data in all files."""
        for file in self.settingDict.values():
            file.save()
        self.settingDict.clear()

    def save(self, name: str):
        """Saves data."""
        self.settingDict.get(name).save()

    def get(self, name: str) -> DataFile:
        """Gets datafile object."""
        return self.settingDict.get(name)
