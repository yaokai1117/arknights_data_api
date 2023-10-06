import json
import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from data_cleaning import process_data
from per_table_data_cleaning import filename_to_process_func, DataProcessingContext
from utils.mongo_client import MongoClient

DATA_DIR_NAME = 'data'

# Directory containing the JSON files
dirname = os.path.join(ROOT_PATH, DATA_DIR_NAME)

# List of JSON file names (without the .json extension) to be stored to MongoDB.
#
# Note: The order of this list matters. We may use context provided from an
# earlier table to process a later table.
json_filenames = [
    'item_table',
    'character_table',
    'skill_table',
    ] 

data_processing_context = DataProcessingContext()

def update_mongo_db() -> None:
    mongo_client = MongoClient()
    for filename in json_filenames:
        collection_name = filename

        json_file_path = os.path.join(dirname, f'{filename}.json')

        # Read the JSON file and insert its contents into the collection
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            process_data(data)
            if filename in filename_to_process_func.keys():
                data = filename_to_process_func[filename](data, data_processing_context)
            mongo_client.create_or_replace_collection(collection_name, data)

        print(f"Collection '{collection_name}' created/updated with data from '{json_file_path}'")

    mongo_client.close()


if __name__ == '__main__':
    update_mongo_db()
