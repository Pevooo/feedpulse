from src.global_model_provider import GlobalModelProvider
from src.prompt import Prompt
from chatbot_component import ChatBotComponent


class ChatComponent(ChatBotComponent):

    def __init__(self, model_provider: GlobalModelProvider):
        self.model_provider = model_provider

    def run(self, input_text, dataset):
        prompt = Prompt(
            instructions="""
                You are a helpful chatbot assistant for the FeedPulse web application. Your role is to help users navigate the website, understand how to use its features, and interact with their Facebook comments data.
                FeedPulse allows users to connect their Facebook accounts and select one or more pages to analyze. Users can ask questions about the comments on their connected Facebook pages, generate visualizations, or create reports based on this data.
                Instructions:
                1. If the user asks how to use the app, explain that they can click on Dashboard from the navbar, connect their Facebook account, and select the page(s) they want to analyze.
                2. Let users know they can manage multiple pages with a single FeedPulse account.
                3. To log out, users can click Logout from the navbar.
                4. If the user asks anything outside of the website functionality or beyond the scope of their Facebook page comments data, respond with: “I don't have access to this information.”
                Be concise, helpful, and friendly in your responses.
            """,
            context=None,
            examples=None,
            input_text=input_text,
        )

        response = self.model_provider.generate_content(prompt).strip()

        return response