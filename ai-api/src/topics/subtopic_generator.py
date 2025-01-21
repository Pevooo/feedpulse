from src.models.prompt import Prompt
from src.topics.feedback_topic import FeedbackTopic
from src.models.model import Model


class SubtopicGenerator:
    def __init__(self, model: Model):
        self.model = model

    def generate(self, org_description: str) -> tuple[FeedbackTopic, ...]:
        prompt = self._generate_prompt(org_description)
        response = self.model.generate_content(prompt)
        if "NONE" in response:
            return tuple()
        return tuple(map(FeedbackTopic, response.split(",")))

    @staticmethod
    def _generate_prompt(description: str) -> Prompt:
        return Prompt(
            instructions=(
                "You will be given a type of an organization and you have to generate subtopics that may affect its rating and "
                "you have to choose from these subtopics:\n"
                f"{','.join(FeedbackTopic.get_all_topics_as_string())}\n"
                "Choose topics from the subtopics listed above and separate them with a ','\n"
                "If it doesn't relate to any of the topics just output 'NONE'\n"
            ),
            context=None,
            examples=(
                (
                    "Restaurant",
                    "cleanliness,staff,food,location",
                ),
                (
                    "Hotel",
                    "parking,security,entertainment,privacy",
                ),
                (
                    "asfiuqwqcaw",
                    "NONE",
                ),
            ),
            input_text=description,
        )
