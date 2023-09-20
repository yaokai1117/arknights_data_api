from typing import List

import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from utils.types import DataEntry, DataProcessFunction

def generate_only_keep_userful_fields_func(useful_fields: List[str]) -> DataProcessFunction:
    return lambda data : {key: value for key, value in data.items() if key in useful_fields}

def process_character_table(input_data: DataEntry) -> List[DataEntry]:
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
    useful_data = generate_only_keep_userful_fields_func(useful_fields)
    return [{'characterPrefabKey': name, **useful_data(data)} for name, data in input_data.items()]

def process_skill_table(input_data: DataEntry) -> List[DataEntry]:
    output = []
    useful_data = generate_only_keep_userful_fields_func(['levels'])
    for name, data in input_data.items():
        data = useful_data(data)
        each_level_useful_data = generate_only_keep_userful_fields_func([
            'name',
            'description',
            'skillType',
            'durationType',
            'spData',
            'duration',
        ])
        data['levels'] = [each_level_useful_data(level) for level in data['levels']]
        output.append({'skillId': name, **data})
    return output

filename_to_process_func = {
    'character_table': process_character_table,
    'skill_table': process_skill_table,
}    
