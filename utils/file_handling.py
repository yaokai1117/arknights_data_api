import json
import os
import requests

from typing import Dict

def save_dict_to_json(data_dict: object, dirname: str, filename: str) -> None:
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    file_path = os.path.join(dirname, filename)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, indent=4, ensure_ascii=False)

def load_dict_from_json(file_path: str) -> Dict[str, str]:
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data_dict = json.load(json_file)
        return data_dict

def download_file(url: str, dirname: str):
    response = requests.get(url)
    if response.status_code == 200:
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        
        file_name = os.path.basename(url)
        file_path = os.path.join(dirname, file_name)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"File downloaded and saved at: {file_path}")
    else:
        print(f"Failed to download file from URL: {url}")