from dataclasses import dataclass


@dataclass
class DataResult:
    impression: bool
    topics: tuple[str, ...]
