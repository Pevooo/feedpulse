import unittest
from unittest.mock import MagicMock
import pandas as pd
from src.chatbot.visualization_component import VisualizationComponent
from src.models.global_model_provider import GlobalModelProvider

class TestVisualizationComponent(unittest.TestCase):
    def setUp(self):
        # Mock the model provider
        self.mock_model_provider = MagicMock(spec=GlobalModelProvider)
        self.mock_model_provider.generate_content = MagicMock(
            side_effect=lambda prompt: """
import matplotlib.pyplot as plt

def plot():
    countries = ['USA', 'Canada', 'Germany']
    values = [100, 200, 300]
    plt.bar(countries, values)
    plt.xlabel('Country')
    plt.ylabel('Value')
    plt.title('Value by Country')
    plt.show()
plot()
"""
        )

        # Create the component with the mock
        self.component = VisualizationComponent(self.mock_model_provider)

        # Sample dataset for testing
        self.dataset = pd.DataFrame({
            "Country": ["USA", "Canada", "Germany"],
            "Value": [100, 200, 300]
        })

    def test_run_returns_visualization_code(self):
        input_text = "Show the value distribution by country"
        result = self.component.run(input_text, self.dataset)

        # Check that the result is the expected code string
        self.assertIn("plt.bar", result)
        self.assertIn("plt.show()", result)
        self.assertIn("countries", result)

        # Make sure generate_content was called
        self.mock_model_provider.generate_content.assert_called()

if __name__ == "__main__":
    unittest.main()
