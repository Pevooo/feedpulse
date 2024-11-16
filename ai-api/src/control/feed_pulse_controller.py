from typing import Iterable, Optional

from src.control.pipeline_result import PipelineResult
from src.data.context_data_unit import ContextDataUnit
from src.data.data_result import DataResult
from src.data.data_unit import DataUnit
from src.data.main_data_unit import MainDataUnit
from src.data_providers.data_provider import DataProvider
from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.data_providers.x_data_provider import XDataProvider
from src.feedback_classification.feedback_classifier import FeedbackClassifier

from src.topic_detection.topic_detector import TopicDetector


class FeedPulseController:
    def __init__(
        self,
        feedback_classifier: FeedbackClassifier,
        topic_detector: TopicDetector,
        data_provider: DataProvider,
    ):
        self.feedback_classifier = feedback_classifier
        self.topic_detector = topic_detector
        self.data_provider = data_provider

    def run_pipeline(
        self,
        data_units: Iterable[DataUnit],
        all_topics: set[str],
        context: Optional[str] = None,
    ) -> PipelineResult:
        """
        Runs the pipeline for the given data to produce the results

        Args:
            data_units (Iterable[DataUnit]): The data units to run the pipeline on
            all_topics (set[str]): A set of the topics that is related to the organization
            context (str, optional): The context text to use. Defaults to None.
        Returns:
            The pipeline result including information about the data.
        """
        results = PipelineResult(all_topics)
        for data_unit in data_units:
            if isinstance(data_unit, ContextDataUnit):  # Not a feedback
                results.extend(
                    self.run_pipeline(data_unit.children, all_topics, data_unit.text)
                )
            elif isinstance(data_unit, MainDataUnit):  # Is a feed
                results.append(self.process(data_unit, all_topics, context))
        return results

    def process(
        self, data_unit: DataUnit, org_topics: set[str], context: Optional[str] = None
    ) -> Optional[DataResult]:
        """
        Processes the given data unit (classifies and detect topic of the data unit)

        Args:
            data_unit (DataUnit): The data unit to process
            org_topics (tuple[str, ...]): The topics related to the organization
            context (str, optional): The context text to use. Defaults to None.

        Returns:
            An object of type DataResult if the processing is successful or None if the data unit is filtered out
            during the process.
        """
        impression = self.classify(data_unit)
        if impression is None:  # Neutral Text
            return None

        topics = self.detect(data_unit, org_topics, context)
        return DataResult(impression, topics)

    def classify(self, data_unit: DataUnit) -> Optional[bool]:
        """
        Classifies the given data unit if it's a complaint or a compliment
        IMPORTANT NOTE: filters out data units having no topic, and non-feedback data units

        Args:
            data_unit (DataUnit): The data unit to classify

        Returns:
            A boolean indication if the data unit is positive or not, will return None if it's filtered out
        """
        result = self.feedback_classifier(data_unit.text)
        if result.text_type == "neutral" or not result.has_topic:
            return None
        return result.text_type == "compliment"

    def detect(
        self, data_unit: DataUnit, org_topics: set[str], context: Optional[str] = None
    ) -> Optional[tuple[str, ...]]:
        """
        Maps the given data unit to a set of topics
        IMPORTANT NOTE: filters out data units that do not map to any topics of the given topics

        Args:
            data_unit (DataUnit): The data unit to detect its topics
            org_topics (tuple[str, ...]): A set of topics that is related to the organization
            context (str, optional): The context text to use. Defaults to None.
        Returns:
            A tuple of the detected topics as strings
        """
        result = self.topic_detector(data_unit.text, org_topics, context)
        if len(result.topics) == 0:
            return None
        return result.topics

    def get_facebook_data_and_run_pipeline(
        self, page_id: str, org_topics: set[str]
    ) -> PipelineResult:
        if isinstance(self.data_provider, FacebookDataProvider):
            data_provider: FacebookDataProvider = self.data_provider
            data_units = data_provider.get_posts(page_id)
            return self.run_pipeline(data_units, org_topics)

    async def get_x_data_and_run_pipeline(
        self, search_query: str, org_topics: set[str], num_tweets: int = 20
    ) -> PipelineResult:
        if isinstance(self.data_provider, XDataProvider):
            data_provider: XDataProvider = self.data_provider
            data_units = await data_provider.get_tweets(num_tweets, search_query)
            return self.run_pipeline(data_units, org_topics)
