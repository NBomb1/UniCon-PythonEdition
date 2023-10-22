class FailedModule:
    def __init__(self, path: str, reason: str, code_reason: Exception):
        self.path = path
        self.reason = reason
        self.codeReason = code_reason
        print(path, reason, code_reason)
