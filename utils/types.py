from typing import Dict, Any, Callable, Union, List

DataEntry = Dict[str, Any]
DataList = List[Union[DataEntry, Any]]
DataProcessFunction = Callable[[DataEntry], DataEntry]
