from dataclasses import dataclass
from datetime import datetime

from src.data.data_unit import DataUnit


@dataclass
class ContextDataUnit(DataUnit):
    """
    Represents a data unit which we can infer context from (should not be treated as a feedback)
    """

    text: str = None
    time_created: datetime = None
    children: tuple[DataUnit, ...] = None
