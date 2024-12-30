from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DataUnit(ABC):
    """
    an interface for data unit
    """

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @property
    @abstractmethod
    def time_created(self) -> datetime:
        pass

    @property
    @abstractmethod
    def children(self) -> tuple["DataUnit", ...]:
        pass
