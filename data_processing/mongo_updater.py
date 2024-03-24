import os  # nopep8
import sys  # nopep8
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')  # nopep8
sys.path.append(ROOT_PATH)  # nopep8

from utils.mongo_client import MongoClient
from per_table_data_cleaning import filename_to_process_func, DataProcessingContext
from data_cleaning import process_table_data
import json

TABLE_DATA_DIR_NAME = 'data/table'

# Directory containing the table data files
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


if __name__ == '__main__':
    write_table_data_to_db()
