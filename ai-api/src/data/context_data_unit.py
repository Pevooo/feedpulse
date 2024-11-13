from dataclasses import dataclass
from datetime import datetime

from src.data.data_unit import DataUnit


@dataclass
class ContextDataUnit(DataUnit):
    text: str = None
    time_created: datetime = None
    children: tuple[DataUnit, ...] = None
