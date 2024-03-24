import os  # nopep8
import sys  # nopep8
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')  # nopep8
sys.path.append(ROOT_PATH)  # nopep8

from utils.type_def import DataEntry
from typing import Union, List
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

# # Sample JSON data
# data = {
#     'description': '立即获得<@ba.vup>{cost}</>点部署费用，攻击力增加<@ba.vup>+{atk:0%}</>。',
#     'blackboard': [
#         {
#             'key': 'cost',
#             'value': 6.0,
#             'valueStr': None
#         },
#         {
#             'key': 'atk',
#             'value': 0.25,
#             'valueStr': None
#         }
#     ]
# }

# # Process the tags and perform string interpolation
# _process_tags(data)

# # Interpolate the 'valueStr' within the 'blackboard' list
# _process_blackboards(data)

# print(data)

# import os
# from utils import save_dict_to_json, load_dict_from_json
# dirname = os.path.join(os.path.dirname(__file__), '../data')
# test_json_data = load_dict_from_json(os.path.join(dirname, 'character_table.json'))
# _process_tags(test_json_data)
# _process_blackboards(test_json_data)
# save_dict_to_json(test_json_data, os.path.join(dirname, 'test'), 'character_table.json')
