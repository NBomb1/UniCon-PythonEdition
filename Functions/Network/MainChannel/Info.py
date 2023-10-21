"""
Contains special data for Authentication.

Warning: Editing these variables can cause connection problems.
"""
from UI.Info import Info as UIInfo


class Info:
    AuthVersion = "0.0.1"
    SecurityVersion = "0.0.1"
    ModuleAuth = "0.0.1"
    MessageTransfer = "0.0.1"

    unique_message = "ProjectSocketInterface16102023"
    preAuthMessageLength = 128
    defaultPassword = "*GT/;S*:s_.7_G[T8K)0vW6:6=YO+p?R{qU<)V/[hXy]~Rl5$0vC<D;yb#3tR?#gX4@y"

    @staticmethod
    def getBuiltInModules() -> dict:
        return {
            "Auth": Info.AuthVersion,
            "Security": Info.SecurityVersion,
            "ModuleAuth": Info.ModuleAuth,
            "MessageTransfer": Info.MessageTransfer,
            "UI": UIInfo.version
        }
