import pymongo
import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from utils.types import DataEntry
from typing import List, Dict, Any
from ariadne import ObjectType, InputType
from character_bindables import reversed_rarity_map
from dotenv import load_dotenv

# Top lelvel query bindables.

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = 'arknights'

# Mongo db connection
client = pymongo.MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

def filter_to_mongo_query(filter: Dict[str, Any], data_wrapper_map: Dict[str, dict] = {}) -> dict:
    sub_queries = []
    for name, value in filter.items():
        data_wrapper = lambda v: data_wrapper_map[name][v] if name in data_wrapper_map.keys() else v
        if isinstance(value, list):
            sub_queries.extend({name: data_wrapper(v)} for v in value)
        elif value != None: 
            sub_queries.append({name: data_wrapper(value)})

    if len(sub_queries) == 1:
        return sub_queries[0]
    elif len(sub_queries) > 1:
        return {'$and': sub_queries}

    return {}

# Resolvers for Query
query = ObjectType('Query')

@query.field('characters')
def resolve_character(*_, filter: Dict[str, Any]) -> List[DataEntry]:
    collection = db['character_table']
    query = filter_to_mongo_query(filter, data_wrapper_map={'rarity': reversed_rarity_map})
    return collection.find(query)

query_bindables = [
    query,
    InputType('CharacterFilter'),
]
