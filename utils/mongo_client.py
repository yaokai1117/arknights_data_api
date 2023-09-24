import os
import pymongo

from dotenv import load_dotenv
from typing import Union, List
from utils.type_def import DataEntry

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = 'arknights'

class MongoClient:
    def __init__(self) -> None:
        # Connect to MongoDB
        self.client = pymongo.MongoClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]

    def create_or_replace_collection(self, collection_name: str, data: Union[DataEntry, List[DataEntry]]) -> None:
        # Check if the collection already exists and drop it if it does
        if collection_name in self.db.list_collection_names():
            self.db[collection_name].drop()
    
        if isinstance(data, dict):
            self.db[collection_name].insert_one(data)
        elif isinstance(data, list):
            self.db[collection_name].insert_many(data)

    def query_collection(self, collection_name: str, query: dict) -> List[DataEntry]:
        collection = self.db[collection_name]
        return collection.find(query)


    def close(self):
        # Close the MongoDB connection
        self.client.close()