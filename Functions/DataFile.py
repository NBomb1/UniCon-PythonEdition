import yaml


class DataFile:
    data: dict[str: object] = {}

    def __init__(self, path: str):
        self.path = path
        self._loadData()

    def save(self):
        with open(self.path, mode='w') as file:
            yaml.dump(self.data, file)

    def put(self, key: str, value: object):
        self.data[key] = value

    def get(self, key: str) -> object:
        return self.data.get(key)

    def _loadData(self):
        try:
            with open(self.path, mode='r') as file:
                self.data = yaml.load(file, Loader=yaml.FullLoader)
                self.data = self.data if self.data is not None else {}
        except FileNotFoundError:
            pass
        except yaml.YAMLError:
            raise FileExistsError("File doesn't have yaml syntax or corrupted.")
