import json
from threading import Thread
from urllib.request import Request, urlopen

from Functions.Starting.UpdateChecker.result import UpdateCheckResult
timeout = 20


def github_api_request(url, token: str) -> dict:
    request = Request(url)
    request.add_header('Authorization', f'token {token}')
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode())


def get_commits(url: str, owner: str, repo_name: str, branch: str, token: str, page: int | None = None) -> dict:
    url = f'{url}/repos/{owner}/{repo_name}/commits' + (f'?sha={branch}' if page is None else f'?page={page}')
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
        attributeName: str,
        owner: str,
        repo_name: str,
        branch: str,
        urlApi: str,
        include: bool = False,  # Include merge commits in the comparison.
) -> UpdateCheckResult | None:
    output = []
    try:
        thread = Thread(target=lambda: findChanges(
            currentVersion,
            urlApi,
            owner,
            repo_name,
            branch,
            gitHubToken,
            include,
            output
        ),
                        daemon=True)
        thread.start()
        latest_version = get_latest_version(url, gitHubToken, className, attributeName)
        if latest_version is not None:
            thread.join()
            res = compare_versions(latest_version, currentVersion)
            res = UpdateCheckResult(
                res is True,
                latest_version,
                ''.join(output)
            )
            return res
    except Exception as e:
        print(e)
        print("Couldn't check for updates")
    return None


def get_latest_version(url: str, gitHubToken: str, className: str, attributeName: str) -> None | str:
    request = Request(url)
    request.add_header('Authorization', f'token {gitHubToken}')
    with urlopen(request, timeout=timeout) as response:
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


def findChanges(currentVer: str, url: str, owner: str, repo_name: str, branch: str, token: str, include=False,
                output: list | None = None) -> str:
    returnStr = ''
    try:
        # commits = res
        changes = []
        page = 1
        while True:
            commits = get_commits(url, owner, repo_name, branch, token, page)
            if not commits and changes:
                return "Could not find changes."
            for commit in commits:
                msg: str = commit['commit']['message'].split('\n')[0]
                # print(msg, currentVer, msg.endswith(currentVer))
                if msg.endswith(currentVer):
                    if include:
                        changes.append(commit)
                    break
                changes.append(commit)
            else:
                page += 1
                continue
            break

        for change in changes:
            returnStr += f'Date: {change["commit"]["author"]["date"]}\n{change["commit"]["message"]}\n\n'
        if output is not None:
            output.append(returnStr)
    except Exception as e:
        pass
    return returnStr
