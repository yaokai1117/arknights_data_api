import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from utils.type_def import DataEntry
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

@character.field('skillRequirements')
def resolve_skill_requirements(obj, *_) -> List[DataEntry]:
    return obj['skills']

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

# Resolvers for SkillRequirement
skill_requirement = ObjectType('SkillRequirement')

@skill_requirement.field('id')
def resolve_id(obj, *_) -> str:
    return obj['skillId']

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

character_bindables = [
    character,
    phase,
    attribute_key_frame,
    skill_requirement,
    proficient_requirement,
]
