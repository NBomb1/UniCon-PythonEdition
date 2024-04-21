from Functions.Exceptions.APIException import APIException
from Functions.Network.ModuleConnector.Server.ConnectionInfo import ConnectionInfo


class ModuleConnector:
    allConnections: list[ConnectionInfo] = []

    def addConnectionServer(self, class_, maxListening: int) -> ConnectionInfo:
        if not class_.defaultNetworkAuth:
            raise APIException.WrongDataGiven("defaultNetworkAuth is set to False.")

        return con
