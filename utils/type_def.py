from typing import Dict, Any, Callable

DataEntry = Dict[str, Any]
DataProcessFunction = Callable[[DataEntry], DataEntry]
