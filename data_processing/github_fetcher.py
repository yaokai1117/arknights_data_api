
import requests
import time
import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from utils.file_handling import save_dict_to_json, load_dict_from_json, download_file
from typing import Dict

# GitHub repository details
GITHUB_REPO_OWNER = 'Kengxxiao'
GITHUB_REPO_NAME = 'ArknightsGameData'
GITHUB_REPO_PATH = 'zh_CN/gamedata/excel'
GITHUB_API_BASE_URL = f'https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{GITHUB_REPO_PATH}'
METADATA_DIR_NAME = 'metadata'
DATA_DIR_NAME = 'data'
FILE_TO_HASH_JSON_PATH = 'filename_to_sha.json'
HEADERS = {'Authorization': 'Bearer'} 

# Other constants
UPDATE_INTERVAL_SECONDS = 300  # 5 minutes
FETCH_PATH = 'fetched_files'

def save_file_hash(data_dict: object) -> None:
    dirname = os.path.join(ROOT_PATH, METADATA_DIR_NAME)
    save_dict_to_json(data_dict, dirname, FILE_TO_HASH_JSON_PATH)

def load_file_hash() -> Dict[str, str]:
    dirname = os.path.join(ROOT_PATH, METADATA_DIR_NAME)
    file_path = os.path.join(dirname, FILE_TO_HASH_JSON_PATH)
    return load_dict_from_json(file_path)

def fetch_repository_info() -> None:
    current_files = load_file_hash()
    response = requests.get(GITHUB_API_BASE_URL)
    dirname = os.path.join(ROOT_PATH, DATA_DIR_NAME)
    if response.status_code == 200:
        entries = response.json()
        for entry in entries:
            filename = entry['name']
            if entry['type'] != 'file' or filename in current_files and entry['sha'] == current_files[filename]:
                continue
            download_url = entry['download_url']
            if download_url == None:
                print(f'No download URL for file: {filename}')
                continue
            download_file(download_url, dirname)
            current_files[filename] = entry['sha']
    save_file_hash(current_files)

def main() -> None:
    if not os.path.exists(FETCH_PATH):
        os.makedirs(FETCH_PATH)

    while True:
        fetch_repository_info()
        print('Refetched latest game data from github.')
        # Trigger another script here (e.g., using subprocess module)
        # subprocess.run(['python', 'path/to/your/script.py'])
        
        time.sleep(UPDATE_INTERVAL_SECONDS)

if __name__ == '__main__':
    main()
