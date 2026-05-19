import datetime
from threading import Thread
from time import sleep

from Functions.Network.FileTransfer.Files.Sending.SendingFileInfo import SendFileInfo


class SendingInfo(list[SendFileInfo]):

    def __init__(self, files: list[str], timeout=15):
        super().__init__()
        for path in files:
            Thread(
                daemon=True,
                target=lambda:
                    self.append(
                        SendFileInfo(
                            path,
                            open(path, 'rb')
                        )
                    )
            ).start()

        # timeout
        timeout = datetime.datetime.now().__add__(datetime.timedelta(0, timeout))
        while timeout > datetime.datetime.now():
            if len(files) == len(self):
                break
            sleep(0.2)
        else:
            raise TimeoutError(f"Operation took too long time. timeout = {timeout}")

    def sending_information_format(self) -> dict:
        text = {}
        for i in self:
            name = i.fullPath.split('/')[-1]
            assert text.get(name) is None, "Can't send files with same name."
            text[name] = i.fullSize
        return text

    def closeAll(self):
        for i in self:
            i.file.close()

    def calculate_bytes_sent(self) -> int:
        return sum(tuple(map(lambda x: x.sentSize, self)))

    def calculate_bytes(self) -> int:
        return sum(tuple(map(lambda x: x.fullSize, self)))
