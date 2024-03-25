import os  # nopep8
import sys  # nopep8
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')  # nopep8
sys.path.append(ROOT_PATH)  # nopep8

from io import StringIO
from utils.type_def import DataEntry
from typing import List

SEGMENT_SIZE_LIMIT = 1000


def process_story_data(raw_data: DataEntry, event_type: str = None) -> List[DataEntry]:
    """Process the json loaded from a story data file, return a list of corpus json.

    Args:
        data (DataEntry): JSON directly loaded from story data file, using utf-8.

    Returns:
        List[DataEntry]: A list of segmented corpus data, the content of each is < 1K characters.
    """
    meta_data_fields = ['eventName', 'storyCode', 'avgTag', 'storyName', 'storyInfo']
    meta_data = {key: value for key, value in raw_data.items() if key in meta_data_fields}
    meta_data['eventType'] = event_type if event_type != None else raw_data['entryType']

    full_list = raw_data['storyList']
    result = []
    segment_index = 0
    buffer: StringIO
    total_length: int

    def initialize_new_segment() -> None:
        nonlocal buffer, total_length
        buffer = StringIO()
        meta_data['segmentIndex'] = segment_index
        meta_lines = '\n'.join(f'{key}: {value}' for key, value in meta_data.items()) + '\n\n'
        meta_lines_length = len(meta_lines)
        buffer.write(meta_lines)
        total_length = meta_lines_length

    def dump_new_segment() -> None:
        new_segment = {}
        new_segment.update(meta_data)
        buffer.seek(0)
        new_segment['content'] = buffer.read()
        result.append(new_segment)
        buffer.close()

    initialize_new_segment()
    for index, entry in enumerate(full_list):
        if entry['prop'] == 'name':
            attributes = entry['attributes']
            new_line = f'''{attributes['name']}: {attributes['content']}\n''' if 'name' in attributes else f'''{attributes['content']}\n'''
            if total_length + len(new_line) >= SEGMENT_SIZE_LIMIT:
                dump_new_segment()
                segment_index += 1
                initialize_new_segment()
            buffer.write(new_line)
            total_length += len(new_line)
        if index == len(full_list) - 1:
            dump_new_segment()

    return result


if __name__ == '__main__':
    import json
    file_path = os.path.abspath('D:\\code\\arknights_data_api\\data\\story\\obt\\main\\level_main_10-05_beg.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        raw_data = json.load(json_file)
        result = process_story_data(raw_data)
        for r in result:
            print('>>> New segment')
            print(r)
            print(len(r['content']))
