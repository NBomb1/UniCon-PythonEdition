import os
import sys
import urllib.request
import base64
import json

# URL файла с последней версией
LATEST_VERSION_URL = 'https://raw.githubusercontent.com/NBomb1/1C-project/master/UI/Info.py'
# URL для скачивания архива
DOWNLOAD_URL = 'https://github.com/NBomb1/1C-project/archive/refs/heads/master.zip'
# Путь к файлу текущей версии
CURRENT_VERSION_FILE = 'version.txt'
# Имя класса и атрибута версии
CLASS_NAME = 'Info'
ATTRIBUTE_NAME = 'version'
GITHUB_API_URL = 'https://api.github.com'
REPO_OWNER = 'NBomb1'
REPO_NAME = '1C-project'
BRANCH = 'master'
# Личный токен доступа (запросить у пользователя)
# GITHUB_TOKEN = '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'
GITHUB_TOKEN = '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'
# GITHUB_TOKEN = 'your_personal_access_token_here'


def github_api_request(url):
    request = urllib.request.Request(url)
    request.add_header('Authorization', f'token {GITHUB_TOKEN}')
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())


def get_repo_contents(path=''):
    url = f'{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote(path)}?ref={BRANCH}'
    return github_api_request(url)


def download_file(file_path, download_path):
    url = f'{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote(file_path)}?ref={BRANCH}'
    print(url)
    file_content = github_api_request(url)

    file_data = base64.b64decode(file_content['content'])

    os.makedirs(os.path.dirname(download_path), exist_ok=True)
    with open(download_path, 'wb') as f:
        f.write(file_data)


def download_directory(path='', download_path=''):
    contents = get_repo_contents(path)
    for item in contents:
        print(f'Downloading {item}')
        if item['type'] == 'file':
            download_file(item['path'], os.path.join(download_path, item['path']))
        elif item['type'] == 'dir':
            download_directory(item['path'], download_path)


def update_program():
    download_path = 'new_version'
    download_directory(download_path=download_path)
    print('Все файлы скачаны.')
    # Здесь можно добавить логику перезапуска программы, если нужно


def restart_program():
    print('Перезапуск программы...')
    os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    update_program()
