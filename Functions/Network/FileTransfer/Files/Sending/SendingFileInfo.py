import os
from typing import BinaryIO


class SendFileInfo:
    def __init__(self, fullPath: str, file: BinaryIO):
        self.fullPath = fullPath
        self.name = fullPath.split('\\')[-1]
        self.file = file
        self.fullSize = os.path.getsize(fullPath)
        self.sentSize = 0
        self.progress = 0

        self.trigger: callable = None

    def setTrigger(self, trigger: callable) -> None:
        self.trigger = trigger

    def updateSentSize(self, size: int) -> None:
        self.sentSize += size
        self.progress = self.sentSize / self.fullSize

        if self.trigger:
            self.trigger()
