import os  # nopep8
import sys  # nopep8
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')  # nopep8
sys.path.append(ROOT_PATH)  # nopep8

from itertools import chain
from utils.mongo_client import MongoClient
from data_processing.table_data_cleaning import process_table_data, filename_to_process_func, DataProcessingContext
from data_processing.story_data_cleaning import process_story_data
import json
from typing import Any

TABLE_DATA_DIR_NAME = 'data/table'
table_data_dirname = os.path.join(ROOT_PATH, TABLE_DATA_DIR_NAME)

# List of table data file names (without the .json extension) to be stored to MongoDB.
#
# Note: The order of this list matters. We may use context provided from an
# earlier table to process a later table.
table_data_filenames = [
    'item_table',
    'character_table',
    'skill_table',
]


def write_table_data_to_db() -> None:
    mongo_client = MongoClient()
    data_processing_context = DataProcessingContext()

    # Update db with table data (e.g. operator attributes).
    for filename in table_data_filenames:
        collection_name = filename

        json_file_path = os.path.join(table_data_dirname, f'{filename}.json')

        # Read the table data JSON file and insert its contents into the collection
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            process_table_data(data)
            if filename in filename_to_process_func.keys():
                data = filename_to_process_func[filename](
                    data, data_processing_context)
            mongo_client.create_or_replace_collection(collection_name, data)

        print(
            f"Collection '{collection_name}' created/updated with data from '{json_file_path}'")

    mongo_client.close()


STORY_DATA_DIR_NAME = 'data/story'
story_data_dirname = os.path.join(ROOT_PATH, STORY_DATA_DIR_NAME)
activities_dirname = os.path.join(story_data_dirname, 'activities')
mainline_dirname = os.path.join(story_data_dirname, 'obt/main')
memory_dirname = os.path.join(story_data_dirname, 'obt/memory')


def write_story_data_to_db() -> None:
    mongo_client = MongoClient()
    story_collection = mongo_client.db['story']
    existing_story = set(_doc_key(doc) for doc in story_collection.find())

    for root, _, filenames in chain(os.walk(activities_dirname), os.walk(mainline_dirname)):
        for filename in filenames:
            path = os.path.join(root, filename)
            with open(path, 'r', encoding='utf-8') as json_file:
                data = process_story_data(json.load(json_file))
                filtered_data = [doc for doc in data
                                 if _doc_key(doc) not in existing_story]
                if len(filtered_data) == 0:
                    continue
                story_collection.insert_many(filtered_data)
                print(f'Update stroty db with data from: {filename}')

    for root, _, filenames in os.walk(memory_dirname):
        for filename in filenames:
            path = os.path.join(root, filename)
            with open(path, 'r', encoding='utf-8') as json_file:
                data = process_story_data(json.load(json_file), event_type='MEMORY')
                filtered_data = [doc for doc in data
                                 if _doc_key(doc) not in existing_story]
                if len(filtered_data) == 0:
                    continue
                story_collection.insert_many(filtered_data)
                print(f'Update stroty db with data from: {filename}')

    mongo_client.close()


def _doc_key(document: dict) -> str:
    return _if_none(document['eventName'], '') + _if_none(document['storyCode'], '') + _if_none(document['avgTag'], '')


def _if_none(value: Any, default_value: Any) -> Any:
    return value if value != None else default_value


if __name__ == '__main__':
    # write_table_data_to_db()
    write_story_data_to_db()
