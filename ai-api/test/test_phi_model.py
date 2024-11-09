import unittest
from src.loaded_models.phi_model import PhiModel

class TestPhiModel(unittest.TestCase):
    """
    def test_connection(self):
        try:
            PhiModel()
        except Exception as e:
            self.fail(f"Connection Failed: {e}")
    """
    def test_str_value(self):
        model = PhiModel()

        result = model.generate_content("The food taste was great")
        #print(result)
        self.assertNotEqual(len(result), 0)