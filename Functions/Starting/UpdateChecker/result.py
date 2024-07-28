class UpdateCheckResult:
    def __init__(self, isOutdated: bool | None, newVersion: str | None, changelog: str | None = None):
        self.isOutdated = isOutdated
        self.newVersion = newVersion
        self.changelog = changelog
