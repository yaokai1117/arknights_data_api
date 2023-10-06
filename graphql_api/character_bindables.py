import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from utils.type_def import DataEntry    
from shared_instances import mongo_client
from typing import List
from ariadne import ObjectType

# Bindables for Character.

rarity_map = {
    'TIER_1': 1,
    'TIER_2': 2,
    'TIER_3': 3,
    'TIER_4': 4,
    'TIER_5': 5,
    'TIER_6': 6,
}
reversed_rarity_map = {value: key for key, value in rarity_map.items()}

phase_map = {
    'PHASE_0': 0,
    'PHASE_1': 1,
    'PHASE_2': 2,
}
reversed_phase_map = {value: key for key, value in phase_map.items()}

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

@character.field('skills')
def resolve_skills(obj, info, index: int = None, *_) -> List[DataEntry]:
    skill_ids = [skill['skillId'] for skill in obj['skills']]
    query = {'skillId': {'$in': skill_ids}}
    skills = mongo_client.query_collection('skill_table', query)
    if index == None or len(skills) == 0:
        return skills
    else:
        return [skills[index % len(skills)]]

@character.field('phases')
def resolve_phases(obj, info, index: int = None, *_) -> int:
    phases = obj['phases']
    if index == None or len(phases) == 0:
        return phases
    else:
        return [phases[index % len(phases)]]


# Resolvers for Phase
phase = ObjectType('Phase')

@phase.field('attributesKeyFrames')
def resolve_attributes_key_frames(obj, info, index: int = None, *_) -> List[DataEntry]:
    frames = []
    for frame_raw_obj in obj['attributesKeyFrames']:
        data = frame_raw_obj['data']
        frames.append({'level': frame_raw_obj['level'],  **data})
    
    if index == None or len(frames) == 0:
        return frames
    else:
        return [frames[index % len(frames)]]

# Resolvers for AttributesKeyFrame
attribute_key_frame = ObjectType('AttributesKeyFrame')

@attribute_key_frame.field('physicalDef')
def resolve_physical_defy(obj, *_) -> int:
    return obj['def']

# Resolvers for SkillRequirement
skill_requirement = ObjectType('SkillRequirement')

@skill_requirement.field('skill')
def resolve_skill_from_requirement(obj, *_) -> DataEntry:
    skill_id = obj['skillId']
    query = {'skillId': skill_id}
    skill_results = mongo_client.query_collection('skill_table', query)
    return skill_results[0] if len(skill_results) == 1 else {}

@skill_requirement.field('character')
def resolve_character_from_requirement(obj, *_) -> DataEntry:
    char_id = obj['characterId']
    query = {'characterPrefabKey': char_id}
    skill_results = mongo_client.query_collection('character_table', query)
    return skill_results[0] if len(skill_results) == 1 else {}

@skill_requirement.field('proficientRequirements')
def resolve_proficient_requirement(obj, *_) -> List[DataEntry]:
    return obj['levelUpCostCond']

# Resolves for ProficentRequirement
proficient_requirement = ObjectType('ProficientRequirement')

@proficient_requirement.field('timeCost')
def resolve_time_cost(obj, *_) -> int:
    return obj['lvlUpTime']

@proficient_requirement.field('materialCost')
def resolve_material_cost(obj, *_) -> List[DataEntry]:
    return obj['levelUpCost']

# Resolves for MaterialCost
material_cost = ObjectType('MaterialCost')

@material_cost.field('materialId')
def resolve_material_id(obj, *_) -> str:
    return obj['id']

character_bindables = [
    character,
    phase,
    attribute_key_frame,
    skill_requirement,
    proficient_requirement,
    material_cost,
]
