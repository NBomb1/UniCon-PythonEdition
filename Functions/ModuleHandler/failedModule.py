class FailedModule:
    def __init__(self, path: str, reason: str, code_reason: Exception, format_: str,
                 isDisabledManually: bool = False,
                 moduleId: str | None = None
                 ):
        self.path = path
        self.reason = reason
        self.codeReason = code_reason
        self.format_exc = format_
        self.isDisabledManually = isDisabledManually
        self.id_ = moduleId  # contains module id if isDisabledManually is True
