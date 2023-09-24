import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from utils.type_def import DataEntry
from shared_instances import mongo_client
from typing import List
from ariadne import ObjectType

# Top lelvel query bindables.

# Resolvers for Query
skill = ObjectType('Skill')

@skill.field('characters')
def resolve_character(obj, *_) -> List[DataEntry]:
    char_ids = obj['characters']
    query = {'characterPrefabKey': {'$in': char_ids}}
    return mongo_client.query_collection('character_table', query)

# Resolvers for SkillLevel
skill_level = ObjectType('SkillLevel')

@skill_level.field('spType')
def resolve_sp_type(obj, *_) -> str:
    sp_data = obj['spData']
    return sp_data['spType']

@skill_level.field('spCost')
def resolve_sp_cost(obj, *_) -> str:
    sp_data = obj['spData']
    return sp_data['spCost']

@skill_level.field('initialSp')
def resolve_initial_sp(obj, *_) -> str:
    sp_data = obj['spData']
    return sp_data['initSp']

@skill_level.field('maxCharge')
def resolve_max_charge(obj, *_) -> str:
    sp_data = obj['spData']
    return sp_data['maxChargeTime']


skill_bindables = [
    skill,
    skill_level,
]
