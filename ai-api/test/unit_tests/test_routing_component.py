import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from src.chatbot.routing_component import RoutingComponent
from src.models.global_model_provider import GlobalModelProvider


class TestRoutingComponent(unittest.TestCase):
    def setUp(self):
        self.mock_provider = MagicMock(spec=GlobalModelProvider)
        self.dataset = pd.DataFrame(
            {
                "Topic": ["Food", "Health", "Electricity"],
                "Sentiment": [0.2, 0.5, -0.1],
                "Month": ["May", "May", "May"],
            }
        )

    @patch("src.chatbot.chat_component.ChatComponent")
    def test_chat_routing(self, MockChatComponent):
        self.mock_provider.generate_content.return_value = "1"
        mock_instance = MockChatComponent.return_value
        mock_instance.run.return_value = "Hi there!"

        router = RoutingComponent(self.mock_provider)
        response, vis_flag = router.run("Hello!", self.dataset)

        self.assertEqual(response, "Hi there!")
        self.assertEqual(vis_flag, 0)
        MockChatComponent.assert_called_once()

    @patch("src.chatbot.query_component.QueryComponent")
    def test_query_routing(self, MockQueryComponent):
        self.mock_provider.generate_content.return_value = "2"
        mock_instance = MockQueryComponent.return_value
        mock_instance.run.return_value = "Most complaints are about food"

        router = RoutingComponent(self.mock_provider)
        response, vis_flag = router.run(
            "What do people complain about most?", self.dataset
        )

        self.assertEqual(response, "Most complaints are about food")
        self.assertEqual(vis_flag, 0)
        MockQueryComponent.assert_called_once()

    @patch("src.chatbot.visualization_component.VisualizationComponent")
    def test_visualization_routing(self, MockVisComponent):
        self.mock_provider.generate_content.return_value = "3"
        mock_instance = MockVisComponent.return_value
        mock_instance.run.return_value = "<image data>"

        router = RoutingComponent(self.mock_provider)
        response, vis_flag = router.run("Show a bar chart of complaints", self.dataset)

        self.assertEqual(response, "<image data>")
        self.assertEqual(vis_flag, 1)
        MockVisComponent.assert_called_once()

    def test_unrecognizable_input(self):
        self.mock_provider.generate_content.return_value = "not a number"

        router = RoutingComponent(self.mock_provider)
        with self.assertRaises(RuntimeError):
            router.run("asdf$@!", self.dataset)


if __name__ == "__main__":
    unittest.main()
