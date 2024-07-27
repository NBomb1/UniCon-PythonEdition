import json
from urllib.request import Request, urlopen

from Functions.Starting.UpdateChecker.result import UpdateCheckResult


def github_api_request(url, token: str) -> dict:
    request = Request(url)
    request.add_header('Authorization', f'token {token}')
    with urlopen(request) as response:
        return json.loads(response.read().decode())


def get_commits(url: str, owner: str, repo_name: str, branch: str, token: str) -> dict:
    url = f'{url}/repos/{owner}/{repo_name}/commits?sha={branch}'
    commits = github_api_request(url, token=token)
    return commits


def compare_versions(current, internetVersion) -> bool:
    """
    Compares two version strings and returns
    True if the current version is less than the internet version,
    False otherwise.

    Parameters:
    current (str): The current version string to compare.
    internetVersion (str): The internet version string to compare.

    Returns:
    bool: True if the current version is less than the internet version, False otherwise.
    """
    def _compare(v1, v2):
        v1_parts = [int(part) for part in v1.split('.')]
        v2_parts = [int(part) for part in v2.split('.')]
        for a, b in zip(v1_parts, v2_parts):
            if a < b:
                return False
            elif a > b:
                return True
        return None

    return _compare(current, internetVersion)


def check_for_updates(
        url: str,
        gitHubToken: str,
        currentVersion: str,
        className: str,
        attributeName: str
) -> UpdateCheckResult | None:
    latest_version = get_latest_version(url, gitHubToken, className, attributeName)
    if latest_version is not None:
        res = compare_versions(latest_version, currentVersion)
        res = UpdateCheckResult(
            res is True,
            latest_version,
            ''
        )
        return res
    return None


def get_latest_version(url: str, gitHubToken: str, className: str, attributeName: str) -> None | str:
    request = Request(url)
    request.add_header('Authorization', f'token {gitHubToken}')
    with urlopen(request) as response:
        latest_file_content = response.read().decode('utf-8')
        return extract_version_from_content(latest_file_content, className, attributeName)


def extract_version_from_content(content, className: str, attributeName: str) -> None | str:
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith(f'class {className}:'):
            for attr_line in lines:
                if attr_line.strip().startswith(f'{attributeName} ='):
                    return attr_line.split('=')[1].strip().strip('"')
    return None
