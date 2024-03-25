import os  # nopep8
import sys  # nopep8
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')  # nopep8
sys.path.append(ROOT_PATH)  # nopep8

from typing import Dict
from data_processing.mongo_updater import write_table_data_to_db, write_story_data_to_db
from utils.file_handling import save_dict_to_json, load_dict_from_json, download_file, download_file_from_git_url

import requests
import time


# GitHub repository details
TABLE_DATA_REPO_OWNER = 'Kengxxiao'
TABLE_DATA_REPO_NAME = 'ArknightsGameData'
TABLE_DATA_REPO_PATH = 'zh_CN/gamedata/excel'
STORY_DATA_REPO_OWNER = '050644zf'
STORY_DATA_REPO_NAME = 'ArknightsStoryJson'
STORY_DATA_REPO_PATH = 'zh_CN/gamedata/story'

METADATA_DIR_NAME = 'metadata'
TABLE_DATA_DIR_NAME = 'data/table'
STORY_DATA_DIR_NAME = 'data/story'
FILE_TO_HASH_JSON_PATH = 'filename_to_sha.json'
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
HEADERS = {'Authorization': f'Bearer {GITHUB_API_TOKEN}'}

# Other constants
UPDATE_INTERVAL_SECONDS = 300  # 5 minutes


def create_github_content_fetch_url(owner: str, name: str, path: str) -> str:
    return f'https://api.github.com/repos/{owner}/{name}/contents/{path}'


def save_file_hash(data_dict: object) -> None:
    dirname = os.path.join(ROOT_PATH, METADATA_DIR_NAME)
    save_dict_to_json(data_dict, dirname, FILE_TO_HASH_JSON_PATH)


def load_file_hash() -> Dict[str, str]:
    dirname = os.path.join(ROOT_PATH, METADATA_DIR_NAME)
    file_path = os.path.join(dirname, FILE_TO_HASH_JSON_PATH)
    return load_dict_from_json(file_path)


def download_changed_file_and_update_file_hash(
        filename: str, dirname: str, sha: str, url: str, current_files: Dict[str, str],
        is_git_url: bool = False) -> bool:
    if filename in current_files and sha == current_files[filename]:
        return False
    if not is_git_url:
        succeeded = download_file(url, dirname)
    else:
        succeeded = download_file_from_git_url(url, os.path.join(dirname, filename))
    if succeeded:
        current_files[filename] = sha
    return succeeded


# Return true if there are any updates.
def fetch_repository_info(content_fetch_url: str, dirname: str, recursive: bool = False) -> bool:
    current_files = load_file_hash()
    response = requests.get(content_fetch_url, headers=HEADERS)
    dirname = os.path.join(ROOT_PATH, dirname)
    has_udpate = False
    if response.status_code != 200:
        return has_udpate

    entries = response.json()
    for entry in entries:
        filename = entry['name']
        if entry['type'] == 'file':
            has_udpate = download_changed_file_and_update_file_hash(
                filename, dirname, entry['sha'], entry['download_url'], current_files) or has_udpate
        if entry['type'] == 'dir' and recursive:
            git_tree_url = entry['git_url'] + '?recursive=true'
            tree_response = requests.get(git_tree_url, headers=HEADERS)
            if tree_response.status_code != 200:
                continue
            sub_dirname = os.path.join(dirname, filename)
            for sub_entry in tree_response.json()['tree']:
                if sub_entry['type'] != 'blob':
                    continue
                has_udpate = download_changed_file_and_update_file_hash(
                    sub_entry['path'],
                    sub_dirname, sub_entry['sha'],
                    sub_entry['url'],
                    current_files, is_git_url=True) or has_udpate

    save_file_hash(current_files)
    return has_udpate


def main() -> None:
    while True:
        # Fetch and update table data.
        table_data_url = create_github_content_fetch_url(
            TABLE_DATA_REPO_OWNER, TABLE_DATA_REPO_NAME, TABLE_DATA_REPO_PATH)
        has_table_data_update = fetch_repository_info(
            table_data_url, TABLE_DATA_DIR_NAME)
        print('Refetched latest game table data from github.')

        if has_table_data_update:
            print('Writing table data to MongoDB.')
            write_table_data_to_db()
            print('Table data written to db.')

        # Fetch and update story data.
        story_data_url = create_github_content_fetch_url(
            STORY_DATA_REPO_OWNER, STORY_DATA_REPO_NAME, STORY_DATA_REPO_PATH)
        has_story_data_update = fetch_repository_info(
            story_data_url, STORY_DATA_DIR_NAME, recursive=True)
        print('Refetched latest game story data from github.')

        if has_story_data_update:
            print('Writing story data to MongoDB.')
            write_story_data_to_db()
            print('Story data written to db.')

        time.sleep(UPDATE_INTERVAL_SECONDS)


if __name__ == '__main__':
    main()
