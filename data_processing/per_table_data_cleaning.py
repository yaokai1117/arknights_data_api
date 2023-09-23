import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from typing import List, Dict
from utils.types import DataEntry, DataProcessFunction

# Context shared across the processing of differnt json files.
class DataProcessingContext:
    # Map from character ids to skill ids.
    character_to_skills: Dict[str, List[str]] = {}

# Clean each table specifically.
#
# Mostly remove unused fields, and change the dict-like data structure to a list-of-dict.
# Also adding fields like foreign keys, names for easier query.

def keep_useful_fields(useful_fields: List[str]) -> DataProcessFunction:
    return lambda data : {key: value for key, value in data.items() if key in useful_fields}

def process_character_table(input_data: DataEntry, context: DataProcessingContext) -> List[DataEntry]:
    output: List[DataEntry] = []
    useful_fields = [
        'name',
        'description',
        'position',
        'tagList',
        'itemUsage',
        'itemDesc',
        'rarity',
        'profession',
        'subProfessionId',
        'phases',
        'skills',
        'talents',
        'potentialRanks',
        'isNotObtainable',
    ]
    useful_data_filter = keep_useful_fields(useful_fields)
    for char_key, data in input_data.items():
        context.character_to_skills[char_key] = [skill['skillId'] for skill in data['skills']]
        output.append({'characterPrefabKey': char_key, **useful_data_filter(data)})
    return output

def process_skill_table(input_data: DataEntry, context: DataProcessingContext) -> List[DataEntry]:
    output: List[DataEntry] = []
    skill_to_characters: Dict[str, List[str]] = {}
    for char, skills in context.character_to_skills.items():
        for skill in skills:
            if skill not in skill_to_characters.keys():
                skill_to_characters[skill] = []
            skill_to_characters[skill].append(char)
    useful_data_filter = keep_useful_fields(['levels'])
    for skillId, data in input_data.items():
        # Ingore non-character skills.
        if skillId not in skill_to_characters.keys():
            continue
        data = useful_data_filter(data)
        each_level_useful_data_fileter = keep_useful_fields([
            'name',
            'description',
            'skillType',
            'durationType',
            'spData',
            'duration',
        ])
        levels = [each_level_useful_data_fileter(level) for level in data['levels']]
        if len(levels) == 0:
            continue
        data['levels'] = levels
        # List of character ids that has this skill.
        data['characters'] = skill_to_characters[skillId] if skillId in skill_to_characters else []
        # Skill name, for easier query.
        data['skillName'] = levels[0]['name']
        output.append({'skillId': skillId, **data})
    return output

filename_to_process_func = {
    'character_table': process_character_table,
    'skill_table': process_skill_table,
}    
