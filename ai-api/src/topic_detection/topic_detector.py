from src.topic_detection.topic_detector_result import TopicDetectorResult
from src.loaded_models.model import Model

class TopicDetector:
    def __init__(self, model: Model, org_topics: list) -> None:
        self.model = model
        self.org_topics = [topic.lower() for topic in org_topics]
    
    def __call__(self, text: str) -> TopicDetectorResult:
        """
        This Method for detecting matching topics.

        Args:
            text (str): The text to detect.

        Returns:
            TopicDectorResult: Contains the list of detected topics.
        """
        
        response: str = self.model.generate_content(self.wrap_text(text)).lower()
        topics = self.extract_topics(response)
        #return topics
        return TopicDetectorResult(topics)
    
    def extract_topics(self, response: str) -> list:
        detected_topics = [topic for topic in self.org_topics if topic in response]
        return detected_topics
    
    def wrap_text(self, text: str) -> str:
        return (
        "Identify and list only the relevant topics from the provided list that directly relate to the content in the text. "
        f"The available topics are: {', '.join(self.org_topics)}.\n"
        f"Here is the text:\n\"{text}\"."
    )