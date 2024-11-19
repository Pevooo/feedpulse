from dataclasses import dataclass
from datetime import datetime

from src.data.data_unit import DataUnit


@dataclass
class MainDataUnit(DataUnit):
    """
    represents a data unit that should be treated as a feedback
    """

    text: str = None
    time_created: datetime = None
    children: tuple[DataUnit, ...] = None
