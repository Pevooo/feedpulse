import unittest
from unittest.mock import Mock

from src.models.global_model_provider import GlobalModelProvider


class TestGlobalModelProvider(unittest.TestCase):
    def setUp(self):

        # Valid model that return "hi"
        self.mock_valid_model_provider = Mock()
        self.mock_valid_model_provider.generate_content = Mock()
        self.mock_valid_model_provider.generate_content.return_value = "hi"

        # Faulty model providers will raise exceptions
        self.mock_invalid_model_provider = Mock()
        self.mock_invalid_model_provider.generate_content = Mock()
        self.mock_invalid_model_provider.generate_content.side_effect = Exception()

    def test_generate_content_no_available_provider(self):
        provider = GlobalModelProvider(
            [self.mock_invalid_model_provider], 0.01
        )  # Canceling the delay

        with self.assertRaises(Exception):
            provider.generate_content(Mock())

        self.mock_invalid_model_provider.generate_content.assert_called()
        self.assertEqual(
            self.mock_invalid_model_provider.generate_content.call_count, 3
        )

    def test_generate_content_available_provider(self):
        provider = GlobalModelProvider([self.mock_valid_model_provider], 0.1)

        result = provider.generate_content(Mock())

        self.assertEqual(result, "hi")
        self.mock_valid_model_provider.generate_content.assert_called_once()

    def test_generate_content_invalid_then_valid_provider(self):
        provider = GlobalModelProvider(
            [self.mock_invalid_model_provider, self.mock_valid_model_provider], 0.1
        )

        result = provider.generate_content(Mock())

        self.assertEqual(result, "hi")
        self.mock_valid_model_provider.generate_content.assert_called_once()
        self.mock_invalid_model_provider.generate_content.assert_called_once()

    def test_generate_content_valid_then_invalid_provider(self):
        provider = GlobalModelProvider(
            [self.mock_valid_model_provider, self.mock_invalid_model_provider], 0.1
        )

        result = provider.generate_content(Mock())

        self.assertEqual(result, "hi")
        self.mock_valid_model_provider.generate_content.assert_called_once()
        self.mock_invalid_model_provider.generate_content.assert_not_called()
