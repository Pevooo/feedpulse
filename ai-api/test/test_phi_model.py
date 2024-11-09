import unittest
from src.loaded_models.phi_model import PhiModel


class TestPhiModel(unittest.TestCase):
    def test_str_value(self):
        model = PhiModel()

        result = model.generate_content("The food taste was great")
        self.assertNotEqual(len(result), 0)
