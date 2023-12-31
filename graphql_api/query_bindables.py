import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from utils.type_def import DataEntry
from shared_instances import mongo_client
from typing import List, Dict, Any
from ariadne import ObjectType, InputType
from character_bindables import reversed_rarity_map

# Top lelvel query bindables.

def filter_to_mongo_query(filter: Dict[str, Any], key_map: Dict[str, str] = {}, value_map: Dict[str, dict] = {}) -> dict:
    sub_queries = []
    for name, value in filter.items():
        name = key_map.get(name, name)
        value_wrapper = lambda v: value_map.get(name, {}).get(v, v)
        if isinstance(value, list):
            sub_queries.extend({name: value_wrapper(v)} for v in value)
        elif value != None: 
            sub_queries.append({name: value_wrapper(value)})

    if len(sub_queries) == 1:
        return sub_queries[0]
    elif len(sub_queries) > 1:
        return {'$and': sub_queries}

    return {}

# Resolvers for Query
query = ObjectType('Query')

@query.field('characters')
def resolve_characters(*_, filter: Dict[str, Any]) -> List[DataEntry]:
    query = filter_to_mongo_query(filter, key_map={'subProfession': 'subProfessionId'}, value_map={'rarity': reversed_rarity_map})
    return mongo_client.query_collection('character_table', query)

@query.field('skill')
def resolve_skill(*_, filter: Dict[str, str]) -> DataEntry:
    query = filter_to_mongo_query(filter)
    result = mongo_client.query_collection('skill_table', query)
    return result[0] if len(result) == 1 else {}

query_bindables = [
    query,
    InputType('CharacterFilter'),
]
