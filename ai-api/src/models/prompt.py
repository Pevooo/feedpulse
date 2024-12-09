from dataclasses import dataclass


@dataclass
class Prompt:
    """
    This class represents the prompt that will be passed to LLM models.
    (Ensuring maximum accuracy)
    """

    instructions: str
    context: Optiona[str]
    examples: tuple[tuple[str, str], ...]

    def to_text(self) -> str: ...
