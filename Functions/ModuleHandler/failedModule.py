class FailedModule:
    def __init__(self, path: str, reason: str, code_reason: Exception, format_: str):
        self.path = path
        self.reason = reason
        self.codeReason = code_reason
        self.format_exc = format_
