from threading import Thread
from urllib.request import urlopen, Request
from urllib.parse import quote
from base64 import b64decode
from UpdaterInfo import *
import json
import os
from time import sleep

threads = []


def github_api_request(url):
    request = Request(url)
    request.add_header('Authorization', f'token {GITHUB_TOKEN}')
    with urlopen(request) as response:
        return json.loads(response.read().decode())


def get_repo_contents(path=''):
    url = f'{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{quote(path)}?ref={BRANCH}'
    return github_api_request(url)


def download_file(file_path, download_path, logs: callable):
    url = f'{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{quote(file_path)}?ref={BRANCH}'
    file_content = github_api_request(url)

    file_data = b64decode(file_content['content'])

    os.makedirs(os.path.dirname(download_path), exist_ok=True)
    with open(download_path, 'wb') as f:
        f.write(file_data)
    logs(f"Downloaded: {file_path}")


def download_directory(logs: callable, path='', download_path=''):
    contents = get_repo_contents(path)
    for item in contents:
        if item['path'].startswith('.idea'):
            continue  # Skip .idea directory
        if item['type'] == 'file':
            thread = Thread(target=download_file, args=(item['path'], os.path.join(download_path, item['path']), logs))
            threads.append(thread)
            thread.start()
        elif item['type'] == 'dir':
            download_directory(logs, item['path'], download_path)


def update_program(logs: callable):
    download_path = 'new_version'
    logs(f'Downloading to {download_path}...')
    download_directory(logs, download_path=download_path)
    while True:
        if all(not thread.is_alive() for thread in threads):
            break
        sleep(1)
    logs('Download completed.')

