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
    examples: Optional[tuple[tuple[str, str], ...]]
    input_text: str

    def __post_init__(self):
        if self.instructions is None:
            raise ValueError("Instructions cannot be None")
        if self.input_text is None:
            raise ValueError("Input text cannot be None")

    def to_text(self) -> str:
        return (
            f"Instructions: {self.instructions}\n"
            f"{self._get_context()}"
            f"{self._get_examples()}"
            f"Prompt:\n"
            f"{self.input_text}\n"
        )

    def get_system_msg(self) -> str:
        return (
            f"Instructions: {self.instructions}\n"
            f"{self._get_examples()}"
        )

    def _get_context(self):
        return f"Context: {self.context}\n" if self.context else ""

    def _get_examples(self) -> str:
        examples_text = ""
        if self.examples is not None and len(self.examples) > 0:
            examples_text += "Examples:\n"
            for example in self.examples:
                examples_text += f"When provided with {example[0]}, expected output should be {example[1]}\n"

        return examples_text

    __str__ = to_text
    __repr__ = to_text
