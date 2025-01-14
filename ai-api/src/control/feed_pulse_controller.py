from typing import Iterable, Optional

from src.data.pipeline_result import PipelineResult
from src.data.feedback_result import FeedbackResult
from src.data.data_unit import DataUnit
from src.data.feedback_data_unit import FeedbackDataUnit
from src.data_providers.data_provider import DataProvider
from src.data_providers.facebook_data_provider import FacebookDataProvider
from src.feedback_classification.feedback_classifier import FeedbackClassifier
from src.reports.report_handler import ReportHandler
from src.topic_detection.topic_detector import TopicDetector


class FeedPulseController:
    """
    Controller for managing the flow of the AI API. It links the Flask app with
    the project's processing pipeline.
    """

    def __init__(
        self,
        feedback_classifier: FeedbackClassifier,
        topic_detector: TopicDetector,
        data_provider: DataProvider,
        report_handler: ReportHandler,
    ):
        self.feedback_classifier = feedback_classifier
        self.topic_detector = topic_detector
        self.data_provider = data_provider
        self.report_handler = report_handler

    def run_pipeline(
        self,
        data_units: Iterable[DataUnit],
        all_topics: set[str],
        context: Optional[str] = None,
    ) -> PipelineResult:
        """
        Processes the given data units and generates a pipeline result.

        Args:
            data_units (Iterable[DataUnit]): Data units to process.
            all_topics (set[str]): Topics related to the organization.
            context (Optional[str]): Context text for topic detection.

        Returns:
            PipelineResult: Processed results with classified feedback and topics.
        """
        results = PipelineResult(all_topics)

        for data_unit in data_units:
            if isinstance(data_unit, FeedbackDataUnit):  # Process feedback data
                processed_result = self.process(data_unit, all_topics, context)
                if processed_result:
                    results.append(processed_result)

            # Recursively process child data units
            results.extend(
                self.run_pipeline(data_unit.children, all_topics, data_unit.text)
            )

        return results

    def process(
        self, data_unit: DataUnit, org_topics: set[str], context: Optional[str] = None
    ) -> Optional[FeedbackResult]:
        """
        Processes a single data unit by classifying feedback and detecting topics.

        Args:
            data_unit (DataUnit): Data unit to process.
            org_topics (set[str]): Organization-related topics.
            context (Optional[str]): Context text for topic detection.

        Returns:
            Optional[FeedbackResult]: Processed feedback result or None if filtered.
        """
        impression = self.feedback_classifier.classify([data_unit.text])
        if impression[0] is None:  # Skip neutral feedback
            return None

        topics = self.topic_detector.detect([data_unit.text], org_topics, context)
        if not topics[0]:  # Skip if no topics detected
            return None

        return FeedbackResult(impression[0], topics[0])

    def fetch_facebook_data(self) -> tuple[DataUnit, ...]:
        """
        Fetches data from a Facebook page.

        Returns:
            tuple[DataUnit, ...]: Fetched posts as data units.
        """
        if not isinstance(self.data_provider, FacebookDataProvider):
            raise TypeError("Data provider must be an instance of FacebookDataProvider")

        return self.data_provider.get_posts()

    def _run_all_steps(
        self,
        data_units: Iterable[DataUnit],
        org_topics: set[str],
        url: str,
    ) -> None:
        """
        Runs all steps of the pipeline: data processing, report creation, and report delivery.

        Args:
            data_units (Iterable[DataUnit]): Data units to process.
            org_topics (set[str]): Organization-related topics.
            url (str): URL to send the generated report.
        """

        # Step 1: Processing the data
        result = self.run_pipeline(data_units, org_topics)

        # Step 2: Creating the report
        report = self.report_handler.create(result)

        # Step 3: Sending the report to the given URL
        self.report_handler.send_report(report, url)

    def run_all_steps_facebook(self, org_topics: set[str], url: str) -> None:
        """
        Fetches Facebook data, processes it, and delivers a report.

        Args:
            org_topics (set[str]): Organization-related topics.
            url (str): URL to send the generated report.
        """
        data_units = self.fetch_facebook_data()
        self._run_all_steps(data_units, org_topics, url)
