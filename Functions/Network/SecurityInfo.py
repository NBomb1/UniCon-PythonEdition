"""
Contains special data for Authentication.

Warning: Editing these variables can cause connection problems.
"""
from UI.Info import Info as UIInfo


# {'version': 0}, 'text': 'ProjectSocketInterface16102023                                                                                                  ', 'text2': "{'Auth': '0.0.1', 'Security': '0.0.1', 'ModuleAuth': '0.0.1', 'MessageTransfer': '0.0.1', 'UI': '0.0.1'}


class SecurityInfo:
    AuthVersion = "0.0.2"
    SecurityVersion = "0.0.1"
    PingManager = "0.0.2"
    MessageTransfer = "0.0.2"

    unique_message = "ProjectSocketInterface16102023"
    preAuthMessageLength = 256
    preAuthGetAccountInfo = 8192
    defaultPassword = "*GT/;S*:s_.7_G[T8K)0vW6:6=YO+p?R{qU<)V/[hXy]~Rl5$0vC<D;yb#3tR?#gX4@y"

    @staticmethod
    def getBuiltInModules() -> dict:
        return {
            "Auth": SecurityInfo.AuthVersion,
            "Security": SecurityInfo.SecurityVersion,
            "PingManager": SecurityInfo.PingManager,
            "MessageTransfer": SecurityInfo.MessageTransfer,
            "UI": UIInfo.version
        }
