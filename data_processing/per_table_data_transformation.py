from typing import List, Dict, Any, Callable

DataEntry = Dict[str, Any]
DataProcessFunction = Callable[[DataEntry], DataEntry]

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

filename_to_process_func = {
    'character_table': process_character_table,
}    
