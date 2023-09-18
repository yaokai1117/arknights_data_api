from data_cleaning import process_data
from per_table_data_transformation import filename_to_process_func

import json
import os
import pymongo

# Replace with your MongoDB connection details
MONGODB_URI = ''
DATABASE_NAME = 'arknights'
DATA_DIR_NAME = 'data'

# Directory containing the JSON files
dirname = os.path.join(os.path.dirname(__file__), f'../{DATA_DIR_NAME}')

# Connect to MongoDB
client = pymongo.MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

# List of JSON file names (without the .json extension)
json_filenames = ['character_table']  # Add your file names here

for filename in json_filenames:
    collection_name = filename

    json_file_path = os.path.join(dirname, f'{filename}.json')

    # Check if the collection already exists and drop it if it does
    if collection_name in db.list_collection_names():
        db[collection_name].drop()

    # Read the JSON file and insert its contents into the collection
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        process_data(data)
        if filename in filename_to_process_func.keys():
            data = filename_to_process_func[filename](data)
        if isinstance(data, dict):
            db[collection_name].insert_one(data)
        elif isinstance(data, list):
            db[collection_name].insert_many(data)

    print(f"Collection '{collection_name}' created/updated with data from '{json_file_path}'")

# Close the MongoDB connection
client.close()