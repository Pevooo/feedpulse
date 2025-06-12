import unittest
from unittest.mock import MagicMock
from src.chatbot.routing_component import RoutingComponent
from src.chatbot.chat_component import ChatComponent
from src.chatbot.query_component import QueryComponent
from src.chatbot.visualization_component import VisualizationComponent
from src.models.global_model_provider import GlobalModelProvider


class TestChooseComponent(unittest.TestCase):
    def setUp(self):
        self.mock_provider = MagicMock(spec=GlobalModelProvider)
        self.router = RoutingComponent(self.mock_provider)

    def test_choose_chat_component(self):
        component, is_raster = self.router._choose_component("1")
        self.assertIsInstance(component, ChatComponent)
        self.assertEqual(is_raster, 0)

    def test_choose_query_component(self):
        component, is_raster = self.router._choose_component("2")
        self.assertIsInstance(component, QueryComponent)
        self.assertEqual(is_raster, 0)

    def test_choose_visualization_component(self):
        component, is_raster = self.router._choose_component("3")
        self.assertIsInstance(component, VisualizationComponent)
        self.assertEqual(is_raster, 1)

    def test_choose_invalid_int_component(self):
        component, is_raster = self.router._choose_component("4")
        self.assertIsInstance(component, ChatComponent)
        self.assertEqual(is_raster, 0)

    def test_choose_non_numeric_response(self):
        component, is_raster = self.router._choose_component("Hello!")
        self.assertIsInstance(component, ChatComponent)
        self.assertEqual(is_raster, 0)
