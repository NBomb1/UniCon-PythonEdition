class ServerInformation:
    def __init__(self, ip: str, port: int, password: str):
        self.ip = ip
        self.port = port
        self.participants = []
        self.password = password
        self.modules = []
