import re
import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from typing import List, Dict
from utils.type_def import DataEntry, DataProcessFunction

# Context shared across the processing of differnt json files.
class DataProcessingContext:
    # Map from character ids to skill requiremetns.
    #
    # Need to store this in the shared context because this is
    # a skill info while stored in the character table.
    character_to_skill_requirements: Dict[str, List[DataEntry]] = {}

# Clean each table specifically.
#
# Mostly remove unused fields, and change the dict-like data structure to a list-of-dict.
# Also adding fields like foreign keys, names for easier query.

def keep_useful_fields(useful_fields: List[str]) -> DataProcessFunction:
    return lambda data : {key: value for key, value in data.items() if key in useful_fields}

special_char_in_names = re.compile(r'(\'|\"|\‘|\“|\”|\’|\，|\。|\《|\》|\!|\！|\?|\||\,|\.|\(|\)|\[|\]|\-|\、|\《|\》|\s)')
def remove_special_characters(input: str) -> str:
    return re.sub(special_char_in_names, '', input)

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
        data['name'] = remove_special_characters(data['name'])
        for skill in data['skills']:
            skill['characterId'] = char_key
        context.character_to_skill_requirements[char_key] = data['skills']
        output.append({'characterPrefabKey': char_key, **useful_data_filter(data)})
    return output

def process_skill_table(input_data: DataEntry, context: DataProcessingContext) -> List[DataEntry]:
    output: List[DataEntry] = []
    # Skill id to its proficient requirements in different character.
    # Note that different characters can have the same skill name, but their
    # proficient requiremetns can be different.
    skill_to_reqs: Dict[str, List[DataEntry]] = {}
    for skill_reqs in context.character_to_skill_requirements.values():
        for req in skill_reqs:
            skill_id = req['skillId']
            if skill_id not in skill_to_reqs.keys():
                skill_to_reqs[skill_id] = []
            skill_to_reqs[skill_id].append(req)
    useful_data_filter = keep_useful_fields(['levels'])
    for skillId, data in input_data.items():
        # Ingore non-character skills.
        if skillId not in skill_to_reqs.keys():
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
        levels = []
        for level in data['levels']:
            level['name'] = remove_special_characters(level['name'])
            levels.append(each_level_useful_data_fileter(level))
        if len(levels) == 0:
            continue
        data['levels'] = levels
        # List of character ids that has this skill.
        data['characterIds'] = [req['characterId'] for req in skill_to_reqs[skillId]] if skillId in skill_to_reqs.keys() else []
        # List of proficient requirements (for different characters).
        data['requirements'] = skill_to_reqs[skillId] if skillId in skill_to_reqs.keys() else []
        # Skill name, for easier query.
        data['skillName'] = levels[0]['name']
        output.append({'skillId': skillId, **data})
    return output

filename_to_process_func = {
    'character_table': process_character_table,
    'skill_table': process_skill_table,
}    
