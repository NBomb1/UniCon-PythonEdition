import socket

from Functions.Exceptions.APIException import APIException
from Functions.Network.ModuleConnector.ConnectionInfo import ConnectionInfo


class ModuleConnector:
    allConnections: list[ConnectionInfo] = []

    def addConnection(self, class_, ip: str, port: int):
        if not class_.defaultNetworkAuth:
            raise APIException.WrongDataGiven("defaultNetworkAuth is set to False.")

        self.allConnections.append(ConnectionInfo(

        ))
