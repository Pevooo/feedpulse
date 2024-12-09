from dataclasses import dataclass
from typing import Optional


@dataclass
class Prompt:
    """
    This class represents the prompt that will be passed to LLM models.
    (Ensuring maximum accuracy)
    """

    instructions: str
    context: Optional[str]
    examples: tuple[tuple[str, str], ...]

    def to_text(self) -> str: ...
