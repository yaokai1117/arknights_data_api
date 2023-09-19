import re
import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')

import sys
sys.path.append(ROOT_PATH)

from typing import Union, List, Any
from utils.types import DataEntry, DataList

format_code_map = {
    '0%': '.0%'
}

def interpolate_string(string: str, param_map: List[DataEntry]) -> str:
    for param in param_map:
        key = param['key']
        value = param['value']
        value_str = str(value) if value is not None else ''
        
        # Check if the key with format exists in the string as a placeholder
        pattern = re.compile(rf'\{{{key}(:.*?)?\}}')
        matches = pattern.findall(string)
        
        for match in matches:
            if ':' in match:
                # [match] is the captured string inside of the () of the regex.
                format_spec = format_code_map[match[1:]]
                value_str = format(float(value_str), format_spec)
            string = re.sub(pattern, value_str, string)
            
    return string

def process_blackboards(obj: Union[DataEntry, DataList]) -> None:
    if isinstance(obj, dict):
        if 'description' in obj.keys() and 'blackboard' in obj.keys():
            obj['description'] = interpolate_string(obj['description'], obj['blackboard'])
            del obj['blackboard']
    elif isinstance(obj, list):
        for value in obj:
            if isinstance(value, dict):
                process_tags(value)

def remove_tags(string: str) -> str:
    return re.sub(r'<(@|\$)(\w+)\.(\w+)>(.*?)<\/>', r'\4', string)

def process_tags(obj: Union[DataEntry, DataList]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                obj[key] = remove_tags(value)
            elif isinstance(value, (dict, list)):
                process_tags(value)
    elif isinstance(obj, list):
        for value in obj:
            if isinstance(value, dict):
                process_tags(value)

def process_data(obj: Union[DataEntry, DataList]) -> None:
    process_tags(obj)
    process_blackboards(obj)

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
# process_tags(data)

# # Interpolate the 'valueStr' within the 'blackboard' list
# process_blackboards(data)

# print(data)

# import os
# from utils import save_dict_to_json, load_dict_from_json
# dirname = os.path.join(os.path.dirname(__file__), '../data')
# test_json_data = load_dict_from_json(os.path.join(dirname, 'character_table.json'))
# process_tags(test_json_data)
# process_blackboards(test_json_data)
# save_dict_to_json(test_json_data, os.path.join(dirname, 'test'), 'character_table.json')