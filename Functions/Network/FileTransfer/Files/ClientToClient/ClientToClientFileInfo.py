class ClientToClientFileInfo:
    def __init__(self, name: str, size: int):
        self.name = name
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
