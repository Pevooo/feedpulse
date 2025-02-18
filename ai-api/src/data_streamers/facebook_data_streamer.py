import hashlib
import json
from datetime import datetime, timezone


from src.data_streamers.data_streamer import DataStreamer
from src.spark.spark import SparkTable


class FacebookDataStreamer(DataStreamer):
    """
    represents a data streamer for the Facebook Graph API to preprocess facebook data.
    """

    def stream(self, payload: dict) -> None:
        """
        Process a Facebook Page Comments webhook payload to extract only:
        [page_id, hashed_comment_id, content, timestamp, platform].

        :param payload: JSON payload from the Facebook webhook.
        :return: List of dictionaries containing the extracted fields.
        """
        processed_records = []

        # Iterate over each entry in the payload
        for entry in payload.get("entry", []):
            page_id = entry.get("id")
            changes = entry.get("changes", [])

            for change in changes:
                value = change.get("value", {})
                # Process only if the verb is 'on'
                if value.get("verb") == "on":
                    comment_id = value.get("comment_id")
                    content = value.get("message", "")
                    timestamp = value.get("created_time")

                    # If timestamp is missing in value, fallback to entry's time (convert if numeric)
                    if not timestamp:
                        ts = entry.get("time")
                        if isinstance(ts, int):
                            # Convert from milliseconds to seconds, and create an aware datetime in UTC
                            timestamp = datetime.fromtimestamp(
                                ts / 1000, tz=timezone.utc
                            ).isoformat()
                        else:
                            timestamp = ts

                    # Hash the comment_id if it exists
                    hashed_comment_id = (
                        hashlib.sha256(comment_id.encode("utf-8")).hexdigest()
                        if comment_id
                        else None
                    )

                    # Assemble the record
                    record = {
                        "page_id": page_id,
                        "hashed_comment_id": hashed_comment_id,
                        "content": content,
                        "timestamp": timestamp,
                        "platform": "facebook",
                    }
                    processed_records.append(record)

        with open(SparkTable.INPUT_COMMENTS.value, "w") as json_file:
            json.dump(processed_records, json_file, indent=4)
