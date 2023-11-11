import yaml


class DataFile:
    data: dict[str: object] = {}

    def __init__(self, path: str):
        self._loadData(path)
        self.file = open(path, 'w')

    def close(self):
        yaml.dump(self.data, self.file)
        self.file.close()

    def put(self, key: str, value: object):
        self.data[key] = value

    def get(self, key: str) -> object:
        return self.data.get(key)

    def _loadData(self, path: str):
        try:
            with open(path, mode='r') as file:
                self.data = yaml.load(file, Loader=yaml.FullLoader)
                self.data = self.data if self.data is not None else {}
        except FileNotFoundError:
            pass
