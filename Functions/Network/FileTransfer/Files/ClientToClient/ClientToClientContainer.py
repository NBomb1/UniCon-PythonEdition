from Functions.Network.FileTransfer.Files.ClientToClient.ClientToClientFileInfo import ClientToClientFileInfo


class ClientToClientContainer(list[ClientToClientFileInfo]):
    def __init__(self, files: dict[str, int]):
        """
        Класс для управления информацией о принимаемых файлах.
        """
        super().__init__()
        self.files = files

        for i in files.keys():
            self.append(
                ClientToClientFileInfo(
                    i,
                    files.get(i)
                )
            )

    def sending_information_format(self) -> dict:
        text = {}
        for i in self:
            text[i.name] = i.fullSize
        return text

    def calculate_bytes(self) -> int:
        return sum(self.files.values())

    def calculate_bytes_sent(self) -> int:
        return sum(tuple(map(lambda x: x.receivedSize, self.files)))
