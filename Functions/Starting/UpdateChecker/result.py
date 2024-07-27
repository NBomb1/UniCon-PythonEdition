class UpdateCheckResult:
    def __init__(self, isOutdated: bool, newVersion: str, changelog: str | None = None):
        self.isOutdated = isOutdated
        self.newVersion = newVersion
        self.changelog = changelog
