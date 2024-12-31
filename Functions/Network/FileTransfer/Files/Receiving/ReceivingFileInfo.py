from typing import BinaryIO


class ReceiveFileInfo:
    def __init__(self, fullPath: str, file: BinaryIO, size: int):
        self.fullPath = fullPath
        self.name = fullPath.split('\\')[-1]
        self.file = file
        self.fullSize = size
        self.receivedSize = 0
        self.progress = 0

        self.trigger: callable = None

    def setTrigger(self, trigger: callable) -> None:
        self.trigger = trigger

    def updateSentSize(self, size: int) -> None:
        self.receivedSize += size
        self.progress = self.receivedSize / self.fullSize

        if self.trigger:
            self.trigger()
