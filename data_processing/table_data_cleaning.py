import os  # nopep8
import sys  # nopep8
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')  # nopep8
sys.path.append(ROOT_PATH)  # nopep8

from utils.type_def import DataEntry, DataProcessFunction
from typing import List, Dict, Union
import re


format_code_map = {
    '0%': '.0%',
    '0.0': '.1f',
    '0': '.0f',
    '0.0%': '.1%',
}


def _interpolate_string(string: str, param_map: List[DataEntry]) -> str:
    if string == None:
        return None
    for param in param_map:
        key = param['key']
        value = param['value']

        # Check if the key with format exists in the string as a placeholder
        pattern = re.compile(
            rf'\{{(-?){re.escape(key)}(:.*?)?\}}', re.IGNORECASE)
        matches = pattern.findall(string)

        # [matches] is the captured string inside of the () of the regex.
        for match_group in matches:
            multiplier = -1 if match_group[0] == '-' else 1
            multiplied_value = value * multiplier
            value_str: str = None
            if isinstance(multiplied_value, float):
                format_spec = format_code_map[match_group[1]
                                              [1:]] if ':' in match_group[1] else '.0f'
                value_str = format(multiplied_value, format_spec)
            else:
                value_str = str(multiplied_value)
            string = re.sub(pattern, value_str, string)

    return string


def _process_blackboards(obj: Union[DataEntry, list]) -> None:
    if isinstance(obj, dict):
        if 'description' in obj.keys() and 'blackboard' in obj.keys():
            obj['description'] = _interpolate_string(
                obj['description'], obj['blackboard'])
            del obj['blackboard']
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                _process_blackboards(value)
    elif isinstance(obj, list):
        for value in obj:
            if isinstance(value, (dict, list)):
                _process_blackboards(value)


tag_pattern = re.compile(r'<(@|\$)(\w+)\.(\w+)>(.*?)<\/>')


def _remove_tags(string: str) -> str:
    return re.sub(tag_pattern, r'\4', string)


def _process_tags(obj: Union[DataEntry, list]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                while tag_pattern.search(obj[key]) != None:
                    obj[key] = _remove_tags(obj[key])
            elif isinstance(value, (dict, list)):
                _process_tags(value)
    elif isinstance(obj, list):
        for value in obj:
            if isinstance(value, (dict, list)):
                _process_tags(value)


def process_table_data(obj: Union[DataEntry, list]) -> None:
    _process_tags(obj)
    _process_blackboards(obj)


# Context shared across the processing of differnt json files.
class DataProcessingContext:
    # Map from character ids to skill requiremetns.
    #
    # Need to store this in the shared context because this is
    # a skill info while stored in the character table.
    character_to_skill_requirements: Dict[str, List[DataEntry]] = {}

    item_id_to_name: Dict[str, str] = {}

# Clean each table specifically.
#
# Mostly remove unused fields, and change the dict-like data structure to a list-of-dict.
# Also adding fields like foreign keys, names for easier query.


def _keep_useful_fields(useful_fields: List[str]) -> DataProcessFunction:
    return lambda data: {key: value for key, value in data.items() if key in useful_fields}


special_char_in_names = re.compile(
    r'(\'|\"|\‘|\“|\”|\’|\，|\。|\《|\》|\!|\！|\?|\||\,|\.|\(|\)|\[|\]|\-|\、|\《|\》|\s)')


def _remove_special_characters(input: str) -> str:
    return re.sub(special_char_in_names, '', input)


def _process_character_table(input_data: DataEntry, context: DataProcessingContext) -> List[DataEntry]:
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
    ]
    useful_data_filter = _keep_useful_fields(useful_fields)

    all_profession = [
        'PIONEER',
        'CASTER',
        'SNIPER',
        'WARRIOR',
        'SUPPORT',
        'SPECIAL',
        'MEDIC',
        'TANK'
    ]

    for char_key, data in input_data.items():
        if data['profession'] not in all_profession or data['isNotObtainable'] == True:
            continue
        data['name'] = _remove_special_characters(data['name'])
        for skill in data['skills']:
            # Fill in character id so that we can link to Character from a SkillRequirement.
            skill['characterId'] = char_key
            # Fill in material names.
            for costs in skill['levelUpCostCond']:
                for cost in costs['levelUpCost']:
                    cost_id = cost['id']
                    cost['name'] = context.item_id_to_name.get(
                        cost_id, cost_id)

        for phase in data['phases']:
            if phase['evolveCost'] == None:
                continue
            for cost in phase['evolveCost']:
                cost_id = cost['id']
                cost['name'] = context.item_id_to_name.get(cost_id, cost_id)

        context.character_to_skill_requirements[char_key] = data['skills']
        output.append({'characterPrefabKey': char_key,
                      **useful_data_filter(data)})
    return output


def _process_skill_table(input_data: DataEntry, context: DataProcessingContext) -> List[DataEntry]:
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
    useful_data_filter = _keep_useful_fields(['levels'])
    for skill_id, data in input_data.items():
        # Ingore non-character skills.
        if skill_id not in skill_to_reqs.keys():
            continue
        data = useful_data_filter(data)
        each_level_useful_data_filter = _keep_useful_fields([
            'name',
            'description',
            'skillType',
            'durationType',
            'spData',
            'duration',
        ])
        levels = []
        for level in data['levels']:
            level['name'] = _remove_special_characters(level['name'])
            levels.append(each_level_useful_data_filter(level))
        if len(levels) == 0:
            continue
        data['levels'] = levels
        # List of character ids that has this skill.
        data['characterIds'] = [req['characterId']
                                for req in skill_to_reqs[skill_id]] if skill_id in skill_to_reqs.keys() else []
        # List of proficient requirements (for different characters).
        data['requirements'] = skill_to_reqs[skill_id] if skill_id in skill_to_reqs.keys() else [
        ]
        # Skill name, for easier query.
        data['skillName'] = levels[0]['name']
        output.append({'skillId': skill_id, **data})
    return output


def _process_item_table(input_data: DataEntry, context: DataProcessingContext) -> List[DataEntry]:
    output: List[DataEntry] = []

    items = input_data['items']
    useful_data_filter = _keep_useful_fields(
        ['name', 'description', 'usage', 'obtainApproach'])

    for item_id, data in items.items():
        context.item_id_to_name[item_id] = data['name']
        output.append({'itemId': item_id, **useful_data_filter(data)})
    return output


filename_to_process_func = {
    'character_table': _process_character_table,
    'skill_table': _process_skill_table,
    'item_table': _process_item_table,
}
