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

    def to_text(self) -> str:
        return (
            f"Instructions: {self.instructions}\n"
            f"Context: {self.context}\n"
            "Examples:\n"
            f"{self._get_examples_str()}\n"
        )

    def _get_examples_str(self) -> str:
        examples_text = ""
        for example in self.examples:
            examples_text += f"When provided with {example[0]}, expected output should be {example[1]}\n"

        return examples_text

    __str__ = to_text
    __repr__ = to_text
