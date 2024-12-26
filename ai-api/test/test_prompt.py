import unittest

from src.models.prompt import Prompt


class TestPrompt(unittest.TestCase):
    def test_converting_to_string(self):
        prompt = Prompt(
            instructions="This is the instructions",
            context="This is the Context",
            examples=(
                ("example1", "output1"),
                ("example2", "output2"),
                ("example3", "output3"),
            ),
            input_text="This is the prompt text",
        )

        expected_output = (
            "Instructions: This is the instructions\n"
            "Context: This is the Context\n"
            "Examples:\n"
            "When provided with example1, expected output should be output1\n"
            "When provided with example2, expected output should be output2\n"
            "When provided with example3, expected output should be output3\n"
            "\n"
        )

        self.assertEqual(str(prompt), expected_output)

    def test_converting_to_string_no_context(self):
        prompt = Prompt(
            instructions="This is the instructions",
            context=None,
            examples=(
                ("example1", "output1"),
                ("example2", "output2"),
                ("example3", "output3"),
            ),
            input_text="This is the prompt text",
        )

        expected_output = (
            "Instructions: This is the instructions\n"
            "Context: None\n"
            "Examples:\n"
            "When provided with example1, expected output should be output1\n"
            "When provided with example2, expected output should be output2\n"
            "When provided with example3, expected output should be output3\n"
            "\n"
        )

        self.assertEqual(str(prompt), expected_output)
