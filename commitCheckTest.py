import urllib.request
import json

GITHUB_API_URL = 'https://api.github.com'
REPO_OWNER = 'NBomb1'
REPO_NAME = '1C-project'
BRANCH = 'master'
GITHUB_TOKEN = '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'


def github_api_request(url):
    request = urllib.request.Request(url)
    request.add_header('Authorization', f'token {GITHUB_TOKEN}')
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())


def get_commits():
    url = f'{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/commits?sha={BRANCH}'
    commits = github_api_request(url)
    return commits


def print_commit_info():
    commits = get_commits()
    for commit in commits:
        commit_message = commit['commit']['message']
        commit_date = commit['commit']['author']['date']
        print("-"*32+f'\nДата: {commit_date}, Сообщение: {commit_message}\n{commit.keys()}\n'+'-'*32)


if __name__ == '__main__':
    print_commit_info()
