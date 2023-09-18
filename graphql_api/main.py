from ariadne import load_schema_from_path, make_executable_schema, ObjectType, InputType
from ariadne.asgi import GraphQL
from typing import Any, Dict, List

import os
import pymongo

DataEntry = Dict[str, Any]

# Replace with your MongoDB connection details
MONGODB_URI = ''
DATABASE_NAME = 'arknights'
CHARACTER_TABLE_NAME = 'character_table'

SCHEMA_FILENAME = 'schema.graphql'

# Mongo db connection
client = pymongo.MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

# Load the GraphQL schema from the .graphql file
dirname = os.path.join(os.path.dirname(__file__), SCHEMA_FILENAME)
schema = load_schema_from_path(dirname)

rarity_map = {
    'TIER_1': 1,
    'TIER_2': 2,
    'TIER_3': 3,
    'TIER_4': 4,
    'TIER_5': 5,
    'TIER_6': 6,
}
reversed_rarity_map = {value: key for key, value in rarity_map.items()}

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

@query.field('character')
def resolve_character(*_, name: str) -> DataEntry:
    collection = db[CHARACTER_TABLE_NAME]
    query = filter_to_mongo_query({'name': name}, data_wrapper_map={'rarity': reversed_rarity_map})
    return collection.find_one(query)

@query.field('characters')
def resolve_character(*_, filter: Dict[str, Any]) -> List[DataEntry]:
    collection = db[CHARACTER_TABLE_NAME]
    query = filter_to_mongo_query(filter, data_wrapper_map={'rarity': reversed_rarity_map})
    return collection.find(query)

# Resolvers for Character
character = ObjectType('Character')

@character.field('description')
def resolve_description(obj, *_) -> str:
    return obj['itemUsage'] + '\n' + obj['itemDesc']

@character.field('traits')
def resolve_traits(obj, *_) -> str:
    return obj['description']

@character.field('subProfession')
def resolve_sub_profession(obj, *_) -> str:
    return obj['subProfessionId']

@character.field('rarity')
def resolve_rarity(obj, *_) -> int:
    return rarity_map[obj['rarity']]

@character.field('talents')
def resolve_description(obj, *_) -> List[str]:
    talents = []
    for talent_raw_obj in obj['talents']:
        candidate = talent_raw_obj['candidates'][-1]
        talents.append(candidate['name'] + ': ' + candidate['description'])
    return talents

@character.field('potentialRanks')
def resolve_potential_ranks(obj, *_) -> List[str]:
    return [raw['description'] for raw in obj['potentialRanks']]

# Resolvers for Phase
phase = ObjectType('Phase')

@phase.field('attributesKeyFrames')
def resolve_attributes_key_frames(obj, *_) -> List[DataEntry]:
    frames = []
    for frame_raw_obj in obj['attributesKeyFrames']:
        data = frame_raw_obj['data']
        frames.append({'level': frame_raw_obj['level'],  **data})
    return frames

# Resolvers for AttributesKeyFrame
attribute_key_frame = ObjectType('AttributesKeyFrame')

@attribute_key_frame.field('physicalDef')
def resolve_physical_defy(obj, *_) -> int:
    return obj['def']

bindables = [
    query,
    character,
    phase,
    attribute_key_frame,
    InputType('CharacterFilter'),
]

# Create an executable schema with resolvers
executable_schema = make_executable_schema(schema, *bindables)

# Create an ASGI application
app = GraphQL(executable_schema)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
